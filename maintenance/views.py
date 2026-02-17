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
            messages.success(request, 'Записът за поддръжка е създаден успешно!')
            return redirect('maintenance_detail', pk=maintenance.pk)
    else:
        form = MaintenanceRecordForm()

    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Създай'})


# Maintenance Update
def maintenance_update(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Записът за поддръжка е обновен успешно!')
            return redirect('maintenance_detail', pk=maintenance.pk)
    else:
        form = MaintenanceRecordForm(instance=maintenance)

    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Редактирай'})


# Maintenance Delete
def maintenance_delete(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        messages.success(request, 'Записът за поддръжка е изтрит успешно!')
        return redirect('maintenance_list')

    return render(request, 'maintenance/maintenance_confirm_delete.html', {'maintenance': maintenance})
