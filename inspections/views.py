from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Inspection, InspectionType
from .forms import InspectionForm, InspectionTypeForm
from equipment.models import Equipment


def user_can_create_records(user):
    """Проверява дали потребителят може да създава записи"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile'):
        return user.profile.role in ['admin', 'manager', 'technician', 'operator']
    return False


def user_can_modify(user):
    """Проверява дали може да редактира/изтрива"""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile'):
        return user.profile.role in ['admin', 'manager']
    return False


def inspection_list(request):
    inspections = Inspection.objects.select_related('equipment', 'inspection_type').all()

    equipment_id = request.GET.get('equipment')
    if equipment_id:
        inspections = inspections.filter(equipment_id=equipment_id)

    status = request.GET.get('status')
    if status:
        inspections = inspections.filter(status=status)

    equipment_list = Equipment.objects.all()

    context = {
        'inspections': inspections,
        'equipment_list': equipment_list,
    }
    return render(request, 'inspections/inspection_list.html', context)


def inspection_detail(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    return render(request, 'inspections/inspection_detail.html', {'inspection': inspection})


@login_required
def inspection_create(request):
    if not user_can_create_records(request.user):
        messages.error(request, 'Нямате права да създавате проверки. Само администратори, мениджъри, техници и оператори могат.')
        return redirect('inspections:inspection_list')

    if request.method == 'POST':
        form = InspectionForm(request.POST, user=request.user)
        if form.is_valid():
            inspection = form.save(commit=False)
            # Ако потребителят е техник и полето е празно, задай го автоматично
            if not inspection.technician and hasattr(request.user, 'technician_profile'):
                inspection.technician = request.user.technician_profile
            inspection.save()
            messages.success(request, 'Проверката е записана успешно!')
            return redirect('inspections:inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm(user=request.user)

    return render(request, 'inspections/inspection_form.html', {'form': form, 'action': 'Създай'})


@login_required
def inspection_update(request, pk):
    if not user_can_modify(request.user):
        messages.error(request, 'Нямате права да редактирате проверки. Само администратори и мениджъри могат.')
        return redirect('inspections:inspection_detail', pk=pk)

    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проверката е актуализирана успешно!')
            return redirect('inspections:inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm(instance=inspection, user=request.user)

    return render(request, 'inspections/inspection_form.html', {'form': form, 'action': 'Редактирай'})


@login_required
def inspection_delete(request, pk):
    if not user_can_modify(request.user):
        messages.error(request, 'Нямате права да изтривате проверки. Само администратори и мениджъри могат.')
        return redirect('inspections:inspection_detail', pk=pk)

    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        inspection.delete()
        messages.success(request, 'Проверката е изтрита успешно!')
        return redirect('inspections:inspection_list')
    return render(request, 'inspections/inspection_confirm_delete.html', {'inspection': inspection})


def inspection_type_list(request):
    inspection_types = InspectionType.objects.all().order_by('frequency', 'name')
    context = {'inspection_types': inspection_types}
    return render(request, 'inspections/inspection_type_list.html', context)


def inspection_type_detail(request, pk):
    inspection_type = get_object_or_404(InspectionType, pk=pk)
    inspections = inspection_type.inspections.all()[:10]
    context = {
        'inspection_type': inspection_type,
        'inspections': inspections,
    }
    return render(request, 'inspections/inspection_type_detail.html', context)


def inspection_type_create(request):
    if request.method == 'POST':
        form = InspectionTypeForm(request.POST)
        if form.is_valid():
            inspection_type = form.save()
            messages.success(request, f'Тип проверка "{inspection_type.name}" е създаден успешно!')
            return redirect('inspections:inspection_type_detail', pk=inspection_type.pk)
    else:
        form = InspectionTypeForm()

    return render(request, 'inspections/inspection_type_form.html', {'form': form, 'action': 'Създай'})


def inspection_type_update(request, pk):
    inspection_type = get_object_or_404(InspectionType, pk=pk)
    if request.method == 'POST':
        form = InspectionTypeForm(request.POST, instance=inspection_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Тип проверка "{inspection_type.name}" е актуализиран успешно!')
            return redirect('inspections:inspection_type_detail', pk=inspection_type.pk)
    else:
        form = InspectionTypeForm(instance=inspection_type)

    return render(request, 'inspections/inspection_type_form.html',
                  {'form': form, 'action': 'Редактирай', 'inspection_type': inspection_type})


# Inspection Type Delete (DELETE)
def inspection_type_delete(request, pk):
    inspection_type = get_object_or_404(InspectionType, pk=pk)
    if request.method == 'POST':
        name = inspection_type.name
        inspection_type.delete()
        messages.success(request, f'Тип проверка "{name}" е изтрит успешно!')
        return redirect('inspections:inspection_type_list')

    return render(request, 'inspections/inspection_type_confirm_delete.html', {'inspection_type': inspection_type})


