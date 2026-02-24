from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inspection, InspectionType
from .forms import InspectionForm, InspectionTypeForm
from equipment.models import Equipment


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


def inspection_create(request):
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            inspection = form.save()
            messages.success(request, 'Проверката е записана успешно!')
            return redirect('inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm()

    return render(request, 'inspections/inspection_form.html', {'form': form, 'action': 'Създай'})


def inspection_update(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проверката е актуализирана успешно!')
            return redirect('inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm(instance=inspection)

    return render(request, 'inspections/inspection_form.html', {'form': form, 'action': 'Редактирай'})


def inspection_delete(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        inspection.delete()
        messages.success(request, 'Проверката е изтрита успешно!')
        return redirect('inspection_list')
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
            return redirect('inspection_type_detail', pk=inspection_type.pk)
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
            return redirect('inspection_type_detail', pk=inspection_type.pk)
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
        return redirect('inspection_type_list')

    return render(request, 'inspections/inspection_type_confirm_delete.html', {'inspection_type': inspection_type})


