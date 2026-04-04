from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Inspection, InspectionType
from .forms import InspectionForm, InspectionTypeForm
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


# Inspection Views
class InspectionListView(LoginRequiredMixin, ListView):
    """Списък с проверки"""
    model = Inspection
    template_name = 'inspections/inspection_list.html'
    context_object_name = 'inspections'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Inspection.objects.select_related(
            'equipment', 'inspection_type', 'technician'
        ).all()
        
        # Filter by equipment
        equipment_id = self.request.GET.get('equipment')
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        
        # Filter by inspection type
        itype_id = self.request.GET.get('type')
        if itype_id:
            queryset = queryset.filter(inspection_type_id=itype_id)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-inspection_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment_list'] = Equipment.objects.all()
        context['inspection_types'] = InspectionType.objects.all()
        context['status_choices'] = Inspection.STATUS_CHOICES
        return context


class InspectionDetailView(LoginRequiredMixin, DetailView):
    """Детайли за проверка"""
    model = Inspection
    template_name = 'inspections/inspection_detail.html'
    context_object_name = 'inspection'


class InspectionCreateView(UserCanCreateRecordsMixin, LoginRequiredMixin, CreateView):
    """Създаване на проверка"""
    model = Inspection
    form_class = InspectionForm
    template_name = 'inspections/inspection_form.html'
    
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
        return reverse_lazy('inspections:inspection_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Проверката беше създадена успешно!')
        return super().form_valid(form)


class InspectionUpdateView(UserCanCreateRecordsMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на проверка"""
    model = Inspection
    form_class = InspectionForm
    template_name = 'inspections/inspection_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('inspections:inspection_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Проверката беше обновена успешно!')
        return super().form_valid(form)


class InspectionDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на проверка"""
    model = Inspection
    template_name = 'inspections/inspection_confirm_delete.html'
    success_url = reverse_lazy('inspections:inspection_list')
    
    def delete(self, request, *args, **kwargs):
        inspection = self.get_object()
        messages.success(request, f'Проверката от {inspection.inspection_date} беше изтрита успешно!')
        return super().delete(request, *args, **kwargs)


# InspectionType Views
class InspectionTypeListView(LoginRequiredMixin, ListView):
    """Списък с типове проверки"""
    model = InspectionType
    template_name = 'inspections/inspectiontype_list.html'
    context_object_name = 'inspection_types'
    paginate_by = 20


class InspectionTypeDetailView(LoginRequiredMixin, DetailView):
    """Детайли за тип проверка"""
    model = InspectionType
    template_name = 'inspections/inspectiontype_detail.html'
    context_object_name = 'inspection_type'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itype = self.get_object()
        context['inspections'] = itype.inspections.select_related('equipment', 'technician').order_by('-inspection_date')[:20]
        return context


class InspectionTypeCreateView(UserCanModifyMixin, LoginRequiredMixin, CreateView):
    """Създаване на тип проверка"""
    model = InspectionType
    form_class = InspectionTypeForm
    template_name = 'inspections/inspectiontype_form.html'
    success_url = reverse_lazy('inspections:inspection_type_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Типът проверка {form.instance.name} беше създаден успешно!')
        return super().form_valid(form)


class InspectionTypeUpdateView(UserCanModifyMixin, LoginRequiredMixin, UpdateView):
    """Редактиране на тип проверка"""
    model = InspectionType
    form_class = InspectionTypeForm
    template_name = 'inspections/inspectiontype_form.html'
    
    def get_success_url(self):
        return reverse_lazy('inspections:inspection_type_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Типът проверка {form.instance.name} беше обновен успешно!')
        return super().form_valid(form)


class InspectionTypeDeleteView(UserCanModifyMixin, LoginRequiredMixin, DeleteView):
    """Изтриване на тип проверка"""
    model = InspectionType
    template_name = 'inspections/inspectiontype_confirm_delete.html'
    success_url = reverse_lazy('inspections:inspection_type_list')
    
    def delete(self, request, *args, **kwargs):
        itype = self.get_object()
        messages.success(request, f'Типът проверка {itype.name} беше изтрит успешно!')
        return super().delete(request, *args, **kwargs)


# Backwards compatibility - assign CBVs to old function names
inspection_list = InspectionListView.as_view()
inspection_detail = InspectionDetailView.as_view()
inspection_create = InspectionCreateView.as_view()
inspection_update = InspectionUpdateView.as_view()
inspection_delete = InspectionDeleteView.as_view()
inspection_type_list = InspectionTypeListView.as_view()
inspection_type_detail = InspectionTypeDetailView.as_view()
inspection_type_create = InspectionTypeCreateView.as_view()
inspection_type_update = InspectionTypeUpdateView.as_view()
inspection_type_delete = InspectionTypeDeleteView.as_view()

