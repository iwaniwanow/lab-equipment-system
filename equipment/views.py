from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Equipment, EquipmentCategory
from .forms import EquipmentForm, EquipmentCategoryForm


# Dashboard
def dashboard(request):
    total_equipment = Equipment.objects.count()
    operational = Equipment.objects.filter(status='operational').count()
    maintenance = Equipment.objects.filter(status='maintenance').count()

    context = {
        'total_equipment': total_equipment,
        'operational': operational,
        'maintenance': maintenance,
    }
    return render(request, 'equipment/dashboard.html', context)


# Equipment List (READ)
def equipment_list(request):
    equipment = Equipment.objects.select_related('category').all()
    categories = EquipmentCategory.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        equipment = equipment.filter(category_id=category_id)

    # Filter by status
    status = request.GET.get('status')
    if status:
        equipment = equipment.filter(status=status)

    context = {
        'equipment': equipment,
        'categories': categories,
    }
    return render(request, 'equipment/equipment_list.html', context)


# Equipment Detail (READ)
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    inspections = equipment.inspections.all()[:5]
    maintenance_records = equipment.maintenance_records.all()[:5]

    context = {
        'equipment': equipment,
        'inspections': inspections,
        'maintenance_records': maintenance_records,
    }
    return render(request, 'equipment/equipment_detail.html', context)


# Equipment Create (CREATE)
def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, f'Оборудване {equipment.asset_number} създадено успешно!')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()

    return render(request, 'equipment/equipment_form.html', {'form': form, 'action': 'Създай'})


# Equipment Update (UPDATE)
def equipment_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Оборудване {equipment.asset_number} обновено успешно!')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'equipment/equipment_form.html',
                  {'form': form, 'action': 'Редактирай', 'equipment': equipment})


# Equipment Delete (DELETE)
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        asset_number = equipment.asset_number
        equipment.delete()
        messages.success(request, f'Оборудване {asset_number} изтрито успешно!')
        return redirect('equipment_list')

    return render(request, 'equipment/equipment_confirm_delete.html', {'equipment': equipment})
