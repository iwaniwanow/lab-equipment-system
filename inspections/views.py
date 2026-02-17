from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inspection, InspectionType
from .forms import InspectionForm, InspectionTypeForm
from equipment.models import Equipment


# Inspection List
def inspection_list(request):
    inspections = Inspection.objects.select_related('equipment', 'inspection_type').all()

    # Filter by equipment
    equipment_id = request.GET.get('equipment')
    if equipment_id:
        inspections = inspections.filter(equipment_id=equipment_id)

    # Filter by status
    status = request.GET.get('status')
    if status:
        inspections = inspections.filter(status=status)

    equipment_list = Equipment.objects.all()

    context = {
        'inspections': inspections,
        'equipment_list': equipment_list,
    }
    return render(request, 'inspections/inspection_list.html', context)


# Inspection Detail
def inspection_detail(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    return render(request, 'inspections/inspection_detail.html', {'inspection': inspection})


# Inspection Create
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


# Inspection Update
def inspection_update(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проверката е обновена успешно!')
            return redirect('inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm(instance=inspection)

    return render(request, 'inspections/inspection_form.html', {'form': form, 'action': 'Редактирай'})


# Inspection Delete
def inspection_delete(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        inspection.delete()
        messages.success(request, 'Проверката е изтрита успешно!')
        return redirect('inspection_list')
    return render(request, 'inspections/inspection_confirm_delete.html', {'inspection': inspection})
