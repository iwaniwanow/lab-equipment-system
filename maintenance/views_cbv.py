from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import MaintenanceRecord, MaintenanceType
from .forms import MaintenanceRecordForm, MaintenanceTypeForm
from equipment.models import Equipment


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
        messages.error(self.request, 'Нямате права за това действие.')
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
        messages.error(self.request, 'Нямате права за създаване на записи.')
        return redirect('equipment:dashboard')


# MaintenanceRecord Views
class MaintenanceListView(LoginRequiredMixin, ListView):
    """Списък със записи за поддръжка"""
    model = MaintenanceRecord
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'maintenance_records'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = MaintenanceRecord.objects.select_related(
            'equipment', 'maintenance_type', 'technician'
        ).all()
        
        # Filter by equipment
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        
        # Filter by maintenance type
        mtype_id = self.request.GET.get('type')
        if mtype_id:
            queryset = queryset.filter(maintenance_type_id=mtype_id)
        
        # Filter by result
        result = self.request.GET.get('result')
        if result:
            queryset = queryset.filter(result=result)
        
        return queryset.order_by('-performed_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment_list'] = Equipment.objects.all()
        context['maintenance_types'] = MaintenanceType.objects.all()
        context['result_choices'] = MaintenanceRecord.RESULT_CHOICES
        return context


class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    """Детайли за запис за поддръжка"""
    model = MaintenanceRecord
    template_name = 'maintenance/maintenance_detail.html'
    context_object_name = 'maintenance'


class MaintenanceCreateView(UserCanCreateRecordsMixin, LoginRequiredMixin, CreateView):
    """Създаване на запис за поддръжка"""
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'maintenance/maintenance_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill equipment if passed in URL
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            initial['equipment'] = equipment_id
        return initial
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('maintenance:maintenance_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Записът за поддръжка беше създаден успешно!')
        return super().form_valid(form)


class MaintenanceUpdateView(UserCanCreateRecordsMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на запис за поддръжка"""
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'maintenance/maintenance_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('maintenance:maintenance_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Записът за поддръжка беше обновен успешно!')
        return super().form_valid(form)


class MaintenanceDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на запис за поддръжка"""
    model = MaintenanceRecord
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance:maintenance_list')
    
    def delete(self, request, *args, **kwargs):
        maintenance = self.get_object()
        messages.success(request, f'Записът за поддръжка от {maintenance.performed_date} беше изтрит успешно!')
        return super().delete(request, *args, **kwargs)


# MaintenanceType Views
class MaintenanceTypeListView(LoginRequiredMixin, ListView):
    """Списък с типове поддръжка"""
    model = MaintenanceType
    template_name = 'maintenance/maintenancetype_list.html'
    context_object_name = 'maintenance_types'
    paginate_by = 20


class MaintenanceTypeDetailView(LoginRequiredMixin, DetailView):
    """Детайли за тип поддръжка"""
    model = MaintenanceType
    template_name = 'maintenance/maintenancetype_detail.html'
    context_object_name = 'maintenance_type'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mtype = self.get_object()
        context['records'] = mtype.records.select_related('equipment', 'technician').order_by('-performed_date')[:20]
        return context


class MaintenanceTypeCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на тип поддръжка"""
    model = MaintenanceType
    form_class = MaintenanceTypeForm
    template_name = 'maintenance/maintenancetype_form.html'
    success_url = reverse_lazy('maintenance:maintenance_type_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Типът поддръжка {form.instance.name} беше създаден успешно!')
        return super().form_valid(form)


class MaintenanceTypeUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на тип поддръжка"""
    model = MaintenanceType
    form_class = MaintenanceTypeForm
    template_name = 'maintenance/maintenancetype_form.html'
    
    def get_success_url(self):
        return reverse_lazy('maintenance:maintenance_type_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Типът поддръжка {form.instance.name} беше обновен успешно!')
        return super().form_valid(form)


class MaintenanceTypeDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на тип поддръжка"""
    model = MaintenanceType
    template_name = 'maintenance/maintenancetype_confirm_delete.html'
    success_url = reverse_lazy('maintenance:maintenance_type_list')
    
    def delete(self, request, *args, **kwargs):
        mtype = self.get_object()
        messages.success(request, f'Типът поддръжка {mtype.name} беше изтрит успешно!')
        return super().delete(request, *args, **kwargs)


# Backwards compatibility - assign CBVs to old function names
maintenance_list = MaintenanceListView.as_view()
maintenance_detail = MaintenanceDetailView.as_view()
maintenance_create = MaintenanceCreateView.as_view()
maintenance_update = MaintenanceUpdateView.as_view()
maintenance_delete = MaintenanceDeleteView.as_view()
maintenance_type_list = MaintenanceTypeListView.as_view()
maintenance_type_detail = MaintenanceTypeDetailView.as_view()
maintenance_type_create = MaintenanceTypeCreateView.as_view()
maintenance_type_update = MaintenanceTypeUpdateView.as_view()
maintenance_type_delete = MaintenanceTypeDeleteView.as_view()

