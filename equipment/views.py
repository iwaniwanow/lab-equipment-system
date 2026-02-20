from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Equipment, EquipmentCategory, Manufacturer
from .forms import EquipmentForm, EquipmentCategoryForm, ManufacturerForm


# Custom 404 handler
def custom_404(request, exception):
    return render(request, 'equipment/404.html', status=404)


# Dashboard
def dashboard(request):
    # Автоматично актуализиране на статусите на всички оборудвания
    for equipment in Equipment.objects.all():
        equipment.update_status()

    total_equipment = Equipment.objects.count()
    active = Equipment.objects.filter(status='active').count()
    pending_validation = Equipment.objects.filter(status='pending_validation').count()
    pending_calibration = Equipment.objects.filter(status='pending_calibration').count()
    pending_technical_review = Equipment.objects.filter(status='pending_technical_review').count()
    pending_multiple = Equipment.objects.filter(status='pending_multiple').count()
    maintenance = Equipment.objects.filter(status='maintenance').count()
    out_of_service = Equipment.objects.filter(status='out_of_service').count()

    # Списъци с оборудване за всеки статус (за бутоните)
    active_equipment = Equipment.objects.filter(status='active')
    pending_validation_equipment = Equipment.objects.filter(status='pending_validation')
    pending_calibration_equipment = Equipment.objects.filter(status='pending_calibration')
    pending_technical_review_equipment = Equipment.objects.filter(status='pending_technical_review')
    pending_multiple_equipment = Equipment.objects.filter(status='pending_multiple')
    maintenance_equipment = Equipment.objects.filter(status='maintenance')
    out_of_service_equipment = Equipment.objects.filter(status='out_of_service')

    context = {
        'total_equipment': total_equipment,
        'active': active,
        'pending_validation': pending_validation,
        'pending_calibration': pending_calibration,
        'pending_technical_review': pending_technical_review,
        'pending_multiple': pending_multiple,
        'maintenance': maintenance,
        'out_of_service': out_of_service,
        # Списъци за бутоните
        'active_equipment': active_equipment,
        'pending_validation_equipment': pending_validation_equipment,
        'pending_calibration_equipment': pending_calibration_equipment,
        'pending_technical_review_equipment': pending_technical_review_equipment,
        'pending_multiple_equipment': pending_multiple_equipment,
        'maintenance_equipment': maintenance_equipment,
        'out_of_service_equipment': out_of_service_equipment,
    }
    return render(request, 'equipment/dashboard.html', context)


# Equipment List (READ)
def equipment_list(request):
    equipment = Equipment.objects.select_related('category', 'manufacturer').all()
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
            messages.success(request, f'Equipment {equipment.asset_number} created successfully!')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()

    return render(request, 'equipment/equipment_form.html', {'form': form, 'action': 'Create'})


# Equipment Update (UPDATE)
def equipment_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Equipment {equipment.asset_number} updated successfully!')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'equipment/equipment_form.html',
                  {'form': form, 'action': 'Update', 'equipment': equipment})


# Equipment Delete (DELETE)
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        asset_number = equipment.asset_number
        equipment.delete()
        messages.success(request, f'Equipment {asset_number} deleted successfully!')
        return redirect('equipment_list')

    return render(request, 'equipment/equipment_confirm_delete.html', {'equipment': equipment})


# ========== MANUFACTURER VIEWS ==========

# Manufacturer List (READ)
def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all().order_by('name')
    context = {'manufacturers': manufacturers}
    return render(request, 'equipment/manufacturer_list.html', context)


# Manufacturer Detail (READ)
def manufacturer_detail(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    equipment_list = manufacturer.equipment.all()
    context = {
        'manufacturer': manufacturer,
        'equipment_list': equipment_list,
    }
    return render(request, 'equipment/manufacturer_detail.html', context)


# Manufacturer Create (CREATE)
def manufacturer_create(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            manufacturer = form.save()
            messages.success(request, f'Manufacturer "{manufacturer.name}" created successfully!')
            return redirect('manufacturer_detail', pk=manufacturer.pk)
    else:
        form = ManufacturerForm()

    return render(request, 'equipment/manufacturer_form.html', {'form': form, 'action': 'Create'})


# Manufacturer Update (UPDATE)
def manufacturer_update(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Manufacturer "{manufacturer.name}" updated successfully!')
            return redirect('manufacturer_detail', pk=manufacturer.pk)
    else:
        form = ManufacturerForm(instance=manufacturer)

    return render(request, 'equipment/manufacturer_form.html',
                  {'form': form, 'action': 'Update', 'manufacturer': manufacturer})


# Manufacturer Delete (DELETE)
def manufacturer_delete(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        name = manufacturer.name
        manufacturer.delete()
        messages.success(request, f'Manufacturer "{name}" deleted successfully!')
        return redirect('manufacturer_list')

    return render(request, 'equipment/manufacturer_confirm_delete.html', {'manufacturer': manufacturer})


# ========== EQUIPMENT CATEGORY VIEWS ==========

# Category List (READ)
def category_list(request):
    categories = EquipmentCategory.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'equipment/category_list.html', context)


# Category Detail (READ)
def category_detail(request, pk):
    category = get_object_or_404(EquipmentCategory, pk=pk)
    equipment_list = category.equipment.all()
    context = {
        'category': category,
        'equipment_list': equipment_list,
    }
    return render(request, 'equipment/category_detail.html', context)


# Category Create (CREATE)
def category_create(request):
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = EquipmentCategoryForm()

    return render(request, 'equipment/category_form.html', {'form': form, 'action': 'Create'})


# Category Update (UPDATE)
def category_update(request, pk):
    category = get_object_or_404(EquipmentCategory, pk=pk)
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = EquipmentCategoryForm(instance=category)

    return render(request, 'equipment/category_form.html',
                  {'form': form, 'action': 'Update', 'category': category})


# Category Delete (DELETE)
def category_delete(request, pk):
    category = get_object_or_404(EquipmentCategory, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted successfully!')
        return redirect('category_list')

    return render(request, 'equipment/category_confirm_delete.html', {'category': category})

