from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MaintenanceRecord, MaintenanceType
from .forms import MaintenanceRecordForm, MaintenanceTypeForm
from equipment.models import Equipment


# Maintenance List
def maintenance_list(request):
    maintenance_records = MaintenanceRecord.objects.select_related(
        'equipment', 'maintenance_type'
    ).all()

    # Filter by equipment
    equipment_id = request.GET.get('equipment')
    if equipment_id:
        maintenance_records = maintenance_records.filter(equipment_id=equipment_id)

    # Filter by type
    maintenance_type = request.GET.get('type')
    if maintenance_type:
        maintenance_records = maintenance_records.filter(
            maintenance_type__type=maintenance_type
        )

    equipment_list = Equipment.objects.all()

    context = {
        'maintenance_records': maintenance_records,
        'equipment_list': equipment_list,
    }
    return render(request, 'maintenance/maintenance_list.html', context)


# Maintenance Detail
def maintenance_detail(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    return render(request, 'maintenance/maintenance_detail.html', {'maintenance': maintenance})


# Maintenance Create
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance = form.save()
            messages.success(request, 'Maintenance record created successfully!')
            return redirect('maintenance_detail', pk=maintenance.pk)
    else:
        form = MaintenanceRecordForm()

    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Create'})


# Maintenance Update
def maintenance_update(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance record updated successfully!')
            return redirect('maintenance_detail', pk=maintenance.pk)
    else:
        form = MaintenanceRecordForm(instance=maintenance)

    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Update'})


# Maintenance Delete
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        messages.success(request, 'Maintenance record deleted successfully!')
        return redirect('maintenance_list')

    return render(request, 'maintenance/maintenance_confirm_delete.html', {'maintenance': maintenance})


# ========== MAINTENANCE TYPE VIEWS ==========

# Maintenance Type List (READ)
def maintenance_type_list(request):
    maintenance_types = MaintenanceType.objects.all().order_by('type', 'name')
    context = {'maintenance_types': maintenance_types}
    return render(request, 'maintenance/maintenance_type_list.html', context)


# Maintenance Type Detail (READ)
def maintenance_type_detail(request, pk):
    maintenance_type = get_object_or_404(MaintenanceType, pk=pk)
    records = maintenance_type.records.all()[:10]
    context = {
        'maintenance_type': maintenance_type,
        'records': records,
    }
    return render(request, 'maintenance/maintenance_type_detail.html', context)


# Maintenance Type Create (CREATE)
def maintenance_type_create(request):
    if request.method == 'POST':
        form = MaintenanceTypeForm(request.POST)
        if form.is_valid():
            maintenance_type = form.save()
            messages.success(request, f'Maintenance Type "{maintenance_type.name}" created successfully!')
            return redirect('maintenance_type_detail', pk=maintenance_type.pk)
    else:
        form = MaintenanceTypeForm()

    return render(request, 'maintenance/maintenance_type_form.html', {'form': form, 'action': 'Create'})


# Maintenance Type Update (UPDATE)
def maintenance_type_update(request, pk):
    maintenance_type = get_object_or_404(MaintenanceType, pk=pk)
    if request.method == 'POST':
        form = MaintenanceTypeForm(request.POST, instance=maintenance_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Maintenance Type "{maintenance_type.name}" updated successfully!')
            return redirect('maintenance_type_detail', pk=maintenance_type.pk)
    else:
        form = MaintenanceTypeForm(instance=maintenance_type)

    return render(request, 'maintenance/maintenance_type_form.html',
                  {'form': form, 'action': 'Update', 'maintenance_type': maintenance_type})


# Maintenance Type Delete (DELETE)
def maintenance_type_delete(request, pk):
    maintenance_type = get_object_or_404(MaintenanceType, pk=pk)
    if request.method == 'POST':
        name = maintenance_type.name
        maintenance_type.delete()
        messages.success(request, f'Maintenance Type "{name}" deleted successfully!')
        return redirect('maintenance_type_list')

    return render(request, 'maintenance/maintenance_type_confirm_delete.html', {'maintenance_type': maintenance_type})


