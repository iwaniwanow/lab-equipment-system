from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.db.models import Q, Count
from .models import Equipment, EquipmentCategory, Manufacturer, Department, Location, Technician
from .forms import EquipmentForm, EquipmentCategoryForm, ManufacturerForm, DepartmentForm, LocationForm, TechnicianForm


# Mixins for permissions
class UserCanModifyMixin(UserPassesTestMixin):
    """Mixin за проверка дали потребителят може да модифицира основни данни"""
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser:
            return True
        if hasattr(self.request.user, 'profile'):
            return self.request.user.profile.role in ['admin', 'manager']
        return False

    def handle_no_permission(self):
        messages.error(self.request, 'Нямате права за това действие. Само администратори и мениджъри могат да променят данни.')
        return redirect('equipment:dashboard')


class UserCanCreateRecordsMixin(UserPassesTestMixin):
    """Mixin за проверка дали потребителят може да създава записи"""
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser:
            return True
        if hasattr(self.request.user, 'profile'):
            return self.request.user.profile.role in ['admin', 'manager', 'technician', 'operator']
        return False

    def handle_no_permission(self):
        messages.error(self.request, 'Нямате права за това действие.')
        return redirect('equipment:dashboard')


# Dashboard View
class DashboardView(TemplateView):
    """Dashboard с общ преглед на оборудването"""
    template_name = 'equipment/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Update all equipment statuses
        for equipment in Equipment.objects.all():
            equipment.update_status()

        # Statistics
        context['total_equipment'] = Equipment.objects.count()
        context['active'] = Equipment.objects.filter(status='active').count()
        context['pending_validation'] = Equipment.objects.filter(status='pending_validation').count()
        context['pending_calibration'] = Equipment.objects.filter(status='pending_calibration').count()
        context['pending_technical_review'] = Equipment.objects.filter(status='pending_technical_review').count()
        context['pending_multiple'] = Equipment.objects.filter(status='pending_multiple').count()
        context['maintenance'] = Equipment.objects.filter(status='maintenance').count()
        context['out_of_service'] = Equipment.objects.filter(status='out_of_service').count()

        # Equipment lists for buttons
        context['active_equipment'] = Equipment.objects.filter(status='active')
        context['pending_validation_equipment'] = Equipment.objects.filter(status='pending_validation')
        context['pending_calibration_equipment'] = Equipment.objects.filter(status='pending_calibration')
        context['pending_technical_review_equipment'] = Equipment.objects.filter(status='pending_technical_review')
        context['pending_multiple_equipment'] = Equipment.objects.filter(status='pending_multiple')
        context['maintenance_equipment'] = Equipment.objects.filter(status='maintenance')
        context['out_of_service_equipment'] = Equipment.objects.filter(status='out_of_service')

        return context


# Equipment Views
class EquipmentListView(ListView):
    """Списък с оборудване"""
    model = Equipment
    template_name = 'equipment/equipment_list.html'
    context_object_name = 'equipment'
    paginate_by = 20

    def get_queryset(self):
        queryset = Equipment.objects.select_related('category', 'manufacturer', 'location').all()

        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(asset_number__icontains=search) |
                Q(serial_number__icontains=search) |
                Q(model__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EquipmentCategory.objects.all()
        context['status_choices'] = Equipment.STATUS_CHOICES
        return context


class EquipmentDetailView(DetailView):
    """Детайли за оборудване"""
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment = self.get_object()
        context['maintenance_records'] = equipment.maintenance_records.select_related('maintenance_type', 'technician').order_by('-performed_date')
        context['inspections'] = equipment.inspections.select_related('inspection_type', 'technician').order_by('-inspection_date')
        context['missing_requirements'] = equipment.get_missing_requirements()
        return context


class EquipmentCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на ново оборудване"""
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:equipment_list')

    def form_valid(self, form):
        messages.success(self.request, f'Оборудването {form.instance.asset_number} беше създадено успешно!')
        return super().form_valid(form)


class EquipmentUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на оборудване"""
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'

    def get_success_url(self):
        return reverse_lazy('equipment:equipment_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Оборудването {form.instance.asset_number} беше обновено успешно!')
        return super().form_valid(form)


class EquipmentDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на оборудване"""
    model = Equipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment:equipment_list')

    def delete(self, request, *args, **kwargs):
        equipment = self.get_object()
        messages.success(request, f'Оборудването {equipment.asset_number} беше изтрито успешно!')
        return super().delete(request, *args, **kwargs)


# Manufacturer Views
class ManufacturerListView(ListView):
    """Списък с производители"""
    model = Manufacturer
    template_name = 'equipment/manufacturer_list.html'
    context_object_name = 'manufacturers'
    paginate_by = 20

    def get_queryset(self):
        queryset = Manufacturer.objects.annotate(equipment_count=Count('equipment'))
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(country__icontains=search)
            )
        return queryset


class ManufacturerDetailView(DetailView):
    """Детайли за производител"""
    model = Manufacturer
    template_name = 'equipment/manufacturer_detail.html'
    context_object_name = 'manufacturer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manufacturer = self.get_object()
        context['equipment'] = manufacturer.equipment.all()
        return context


class ManufacturerCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на производител"""
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'equipment/manufacturer_form.html'
    success_url = reverse_lazy('equipment:manufacturer_list')

    def form_valid(self, form):
        messages.success(self.request, f'Производителят {form.instance.name} беше създаден успешно!')
        return super().form_valid(form)


class ManufacturerUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на производител"""
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'equipment/manufacturer_form.html'

    def get_success_url(self):
        return reverse_lazy('equipment:manufacturer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Производителят {form.instance.name} беше обновен успешно!')
        return super().form_valid(form)


class ManufacturerDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на производител"""
    model = Manufacturer
    template_name = 'equipment/manufacturer_confirm_delete.html'
    success_url = reverse_lazy('equipment:manufacturer_list')

    def delete(self, request, *args, **kwargs):
        manufacturer = self.get_object()
        messages.success(request, f'Производителят {manufacturer.name} беше изтрит успешно!')
        return super().delete(request, *args, **kwargs)


# Category Views
class CategoryListView(ListView):
    """Списък с категории"""
    model = EquipmentCategory
    template_name = 'equipment/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        queryset = EquipmentCategory.objects.annotate(equipment_count=Count('equipment'))
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class CategoryDetailView(DetailView):
    """Детайли за категория"""
    model = EquipmentCategory
    template_name = 'equipment/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['equipment'] = category.equipment.all()
        return context


class CategoryCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на категория"""
    model = EquipmentCategory
    form_class = EquipmentCategoryForm
    template_name = 'equipment/category_form.html'
    success_url = reverse_lazy('equipment:category_list')

    def form_valid(self, form):
        messages.success(self.request, f'Категорията {form.instance.name} беше създадена успешно!')
        return super().form_valid(form)


class CategoryUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на категория"""
    model = EquipmentCategory
    form_class = EquipmentCategoryForm
    template_name = 'equipment/category_form.html'

    def get_success_url(self):
        return reverse_lazy('equipment:category_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Категорията {form.instance.name} беше обновена успешно!')
        return super().form_valid(form)


class CategoryDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на категория"""
    model = EquipmentCategory
    template_name = 'equipment/category_confirm_delete.html'
    success_url = reverse_lazy('equipment:category_list')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(request, f'Категорията {category.name} беше изтрита успешно!')
        return super().delete(request, *args, **kwargs)


# Department Views
class DepartmentListView(LoginRequiredMixin, ListView):
    """Списък с отдели"""
    model = Department
    template_name = 'equipment/department_list.html'
    context_object_name = 'departments'
    paginate_by = 20

    def get_queryset(self):
        queryset = Department.objects.filter(is_active=True).annotate(
            equipment_count=Count('equipment'),
            location_count=Count('locations')
        )
        return queryset


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    """Детайли за отдел"""
    model = Department
    template_name = 'equipment/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        context['locations'] = department.locations.all()
        context['equipment'] = department.equipment.all()
        context['technicians'] = department.technicians.filter(is_active=True)
        return context


class DepartmentCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на отдел"""
    model = Department
    form_class = DepartmentForm
    template_name = 'equipment/department_form.html'
    success_url = reverse_lazy('equipment:department_list')

    def form_valid(self, form):
        messages.success(self.request, f'Отделът {form.instance.name} беше създаден успешно!')
        return super().form_valid(form)


class DepartmentUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на отдел"""
    model = Department
    form_class = DepartmentForm
    template_name = 'equipment/department_form.html'

    def get_success_url(self):
        return reverse_lazy('equipment:department_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Отделът {form.instance.name} беше обновен успешно!')
        return super().form_valid(form)


class DepartmentDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на отдел"""
    model = Department
    template_name = 'equipment/department_confirm_delete.html'
    success_url = reverse_lazy('equipment:department_list')

    def delete(self, request, *args, **kwargs):
        department = self.get_object()
        messages.success(request, f'Отделът {department.name} беше изтрит успешно!')
        return super().delete(request, *args, **kwargs)


# Location Views
class LocationListView(LoginRequiredMixin, ListView):
    """Списък с локации"""
    model = Location
    template_name = 'equipment/location_list.html'
    context_object_name = 'locations'
    paginate_by = 20

    def get_queryset(self):
        queryset = Location.objects.filter(is_active=True).select_related('department').annotate(
            equipment_count=Count('equipment')
        )

        # Filter by department
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.filter(is_active=True)
        context['categories'] = Location.CATEGORY_CHOICES
        return context


class LocationDetailView(LoginRequiredMixin, DetailView):
    """Детайли за локация"""
    model = Location
    template_name = 'equipment/location_detail.html'
    context_object_name = 'location'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.get_object()
        context['equipment'] = location.equipment.all()
        return context


class LocationCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на локация"""
    model = Location
    form_class = LocationForm
    template_name = 'equipment/location_form.html'
    success_url = reverse_lazy('equipment:location_list')

    def form_valid(self, form):
        messages.success(self.request, f'Локацията {form.instance.code} беше създадена успешно!')
        return super().form_valid(form)


class LocationUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на локация"""
    model = Location
    form_class = LocationForm
    template_name = 'equipment/location_form.html'

    def get_success_url(self):
        return reverse_lazy('equipment:location_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Локацията {form.instance.code} беше обновена успешно!')
        return super().form_valid(form)


class LocationDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на локация"""
    model = Location
    template_name = 'equipment/location_confirm_delete.html'
    success_url = reverse_lazy('equipment:location_list')

    def delete(self, request, *args, **kwargs):
        location = self.get_object()
        messages.success(request, f'Локацията {location.code} беше изтрита успешно!')
        return super().delete(request, *args, **kwargs)


# Technician Views
class TechnicianListView(LoginRequiredMixin, ListView):
    """Списък с техници"""
    model = Technician
    template_name = 'equipment/technician_list.html'
    context_object_name = 'technicians'
    paginate_by = 20

    def get_queryset(self):
        queryset = Technician.objects.filter(is_active=True).select_related('department', 'user')

        # Filter by department
        department_id = self.request.GET.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        # Filter by specialization
        specialization = self.request.GET.get('specialization')
        if specialization:
            queryset = queryset.filter(specialization=specialization)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.filter(is_active=True)
        context['specializations'] = Technician.SPECIALIZATION_CHOICES
        return context


class TechnicianDetailView(LoginRequiredMixin, DetailView):
    """Детайли за техник"""
    model = Technician
    template_name = 'equipment/technician_detail.html'
    context_object_name = 'technician'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        technician = self.get_object()
        context['maintenance_records'] = technician.maintenance_records.select_related('equipment', 'maintenance_type').order_by('-performed_date')[:10]
        context['inspections'] = technician.inspections.select_related('equipment', 'inspection_type').order_by('-inspection_date')[:10]
        return context


class TechnicianCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на техник"""
    model = Technician
    form_class = TechnicianForm
    template_name = 'equipment/technician_form.html'
    success_url = reverse_lazy('equipment:technician_list')

    def form_valid(self, form):
        messages.success(self.request, f'Техникът {form.instance.get_full_name()} беше създаден успешно!')
        return super().form_valid(form)


class TechnicianUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на техник"""
    model = Technician
    form_class = TechnicianForm
    template_name = 'equipment/technician_form.html'

    def get_success_url(self):
        return reverse_lazy('equipment:technician_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f'Техникът {form.instance.get_full_name()} беше обновен успешно!')
        return super().form_valid(form)


class TechnicianDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на техник"""
    model = Technician
    template_name = 'equipment/technician_confirm_delete.html'
    success_url = reverse_lazy('equipment:technician_list')

    def delete(self, request, *args, **kwargs):
        technician = self.get_object()
        messages.success(request, f'Техникът {technician.get_full_name()} беше изтрит успешно!')
        return super().delete(request, *args, **kwargs)


# Keep old function-based view names for backwards compatibility (will be deprecated)
dashboard = DashboardView.as_view()
equipment_list = EquipmentListView.as_view()
equipment_detail = EquipmentDetailView.as_view()
equipment_create = EquipmentCreateView.as_view()
equipment_update = EquipmentUpdateView.as_view()
equipment_delete = EquipmentDeleteView.as_view()
manufacturer_list = ManufacturerListView.as_view()
manufacturer_detail = ManufacturerDetailView.as_view()
manufacturer_create = ManufacturerCreateView.as_view()
manufacturer_update = ManufacturerUpdateView.as_view()
manufacturer_delete = ManufacturerDeleteView.as_view()
category_list = CategoryListView.as_view()
category_detail = CategoryDetailView.as_view()
category_create = CategoryCreateView.as_view()
category_update = CategoryUpdateView.as_view()
category_delete = CategoryDeleteView.as_view()
department_list = DepartmentListView.as_view()
department_detail = DepartmentDetailView.as_view()
department_create = DepartmentCreateView.as_view()
department_update = DepartmentUpdateView.as_view()
department_delete = DepartmentDeleteView.as_view()
location_list = LocationListView.as_view()
location_detail = LocationDetailView.as_view()
location_create = LocationCreateView.as_view()
location_update = LocationUpdateView.as_view()
location_delete = LocationDeleteView.as_view()
technician_list = TechnicianListView.as_view()
technician_detail = TechnicianDetailView.as_view()
technician_create = TechnicianCreateView.as_view()
technician_update = TechnicianUpdateView.as_view()
technician_delete = TechnicianDeleteView.as_view()

