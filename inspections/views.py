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
            messages.success(request, 'Inspection recorded successfully!')
            return redirect('inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm()

    return render(request, 'inspections/inspection_form.html', {'form': form, 'action': 'Create'})


# Inspection Update
def inspection_update(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        form = InspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inspection updated successfully!')
            return redirect('inspection_detail', pk=inspection.pk)
    else:
        form = InspectionForm(instance=inspection)

    return render(request, 'inspections/inspection_form.html', {'form': form, 'action': 'Update'})


# Inspection Delete
def inspection_delete(request, pk):
    inspection = get_object_or_404(Inspection, pk=pk)
    if request.method == 'POST':
        inspection.delete()
        messages.success(request, 'Inspection deleted successfully!')
        return redirect('inspection_list')
    return render(request, 'inspections/inspection_confirm_delete.html', {'inspection': inspection})


# ========== INSPECTION TYPE VIEWS ==========

# Inspection Type List (READ)
def inspection_type_list(request):
    inspection_types = InspectionType.objects.all().order_by('frequency', 'name')
    context = {'inspection_types': inspection_types}
    return render(request, 'inspections/inspection_type_list.html', context)


# Inspection Type Detail (READ)
def inspection_type_detail(request, pk):
    inspection_type = get_object_or_404(InspectionType, pk=pk)
    inspections = inspection_type.inspections.all()[:10]
    context = {
        'inspection_type': inspection_type,
        'inspections': inspections,
    }
    return render(request, 'inspections/inspection_type_detail.html', context)


# Inspection Type Create (CREATE)
def inspection_type_create(request):
    if request.method == 'POST':
        form = InspectionTypeForm(request.POST)
        if form.is_valid():
            inspection_type = form.save()
            messages.success(request, f'Inspection Type "{inspection_type.name}" created successfully!')
            return redirect('inspection_type_detail', pk=inspection_type.pk)
    else:
        form = InspectionTypeForm()

    return render(request, 'inspections/inspection_type_form.html', {'form': form, 'action': 'Create'})


# Inspection Type Update (UPDATE)
def inspection_type_update(request, pk):
    inspection_type = get_object_or_404(InspectionType, pk=pk)
    if request.method == 'POST':
        form = InspectionTypeForm(request.POST, instance=inspection_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Inspection Type "{inspection_type.name}" updated successfully!')
            return redirect('inspection_type_detail', pk=inspection_type.pk)
    else:
        form = InspectionTypeForm(instance=inspection_type)

    return render(request, 'inspections/inspection_type_form.html',
                  {'form': form, 'action': 'Update', 'inspection_type': inspection_type})


# Inspection Type Delete (DELETE)
def inspection_type_delete(request, pk):
    inspection_type = get_object_or_404(InspectionType, pk=pk)
    if request.method == 'POST':
        name = inspection_type.name
        inspection_type.delete()
        messages.success(request, f'Inspection Type "{name}" deleted successfully!')
        return redirect('inspection_type_list')

    return render(request, 'inspections/inspection_type_confirm_delete.html', {'inspection_type': inspection_type})


