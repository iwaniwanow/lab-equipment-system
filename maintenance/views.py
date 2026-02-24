from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MaintenanceRecord, MaintenanceType
from .forms import MaintenanceRecordForm, MaintenanceTypeForm
from equipment.models import Equipment

def maintenance_list(request):
    maintenance_records = MaintenanceRecord.objects.select_related(
        'equipment', 'maintenance_type'
    ).all()

    equipment_id = request.GET.get('equipment')
    if equipment_id:
        maintenance_records = maintenance_records.filter(equipment_id=equipment_id)

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


def maintenance_detail(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    return render(request, 'maintenance/maintenance_detail.html', {'maintenance': maintenance})


def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance = form.save()
            messages.success(request, f'Записът за поддръжка е създаден успешно! ({maintenance.equipment.asset_number})')
            return redirect('maintenance_detail', pk=maintenance.pk)
        else:
            print("=" * 60)
            print("ГРЕШКИ ВЪВ ФОРМАТА:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
            print("=" * 60)
            messages.error(request, 'Има грешки във формата! Моля, проверете полетата.')
    else:
        form = MaintenanceRecordForm()

    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Създай'})


def maintenance_update(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Записът за поддръжка е актуализиран успешно!')
            return redirect('maintenance_detail', pk=maintenance.pk)
    else:
        form = MaintenanceRecordForm(instance=maintenance)

    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'action': 'Редактирай'})


def maintenance_delete(request, pk):
    maintenance = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        maintenance.delete()
        messages.success(request, 'Записът за поддръжка е изтрит успешно!')
        return redirect('maintenance_list')

    return render(request, 'maintenance/maintenance_confirm_delete.html', {'maintenance': maintenance})


def maintenance_type_list(request):
    maintenance_types = MaintenanceType.objects.all().order_by('type', 'name')
    context = {'maintenance_types': maintenance_types}
    return render(request, 'maintenance/maintenance_type_list.html', context)


def maintenance_type_detail(request, pk):
    maintenance_type = get_object_or_404(MaintenanceType, pk=pk)
    records = maintenance_type.records.all()[:10]
    context = {
        'maintenance_type': maintenance_type,
        'records': records,
    }
    return render(request, 'maintenance/maintenance_type_detail.html', context)


def maintenance_type_create(request):
    if request.method == 'POST':
        form = MaintenanceTypeForm(request.POST)
        if form.is_valid():
            maintenance_type = form.save()
            messages.success(request, f'Тип поддръжка "{maintenance_type.name}" е създаден успешно!')
            return redirect('maintenance_type_detail', pk=maintenance_type.pk)
    else:
        form = MaintenanceTypeForm()

    return render(request, 'maintenance/maintenance_type_form.html', {'form': form, 'action': 'Създай'})


def maintenance_type_update(request, pk):
    maintenance_type = get_object_or_404(MaintenanceType, pk=pk)
    if request.method == 'POST':
        form = MaintenanceTypeForm(request.POST, instance=maintenance_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Тип поддръжка "{maintenance_type.name}" е актуализиран успешно!')
            return redirect('maintenance_type_detail', pk=maintenance_type.pk)
    else:
        form = MaintenanceTypeForm(instance=maintenance_type)

    return render(request, 'maintenance/maintenance_type_form.html',
                  {'form': form, 'action': 'Редактирай', 'maintenance_type': maintenance_type})


def maintenance_type_delete(request, pk):
    maintenance_type = get_object_or_404(MaintenanceType, pk=pk)
    if request.method == 'POST':
        name = maintenance_type.name
        maintenance_type.delete()
        messages.success(request, f'Тип поддръжка "{name}" е изтрит успешно!')
        return redirect('maintenance_type_list')

    return render(request, 'maintenance/maintenance_type_confirm_delete.html', {'maintenance_type': maintenance_type})


