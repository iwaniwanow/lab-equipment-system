from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Equipment, EquipmentCategory, Manufacturer, Department, Location, Technician
from .forms import EquipmentForm, EquipmentCategoryForm, ManufacturerForm, DepartmentForm, LocationForm, TechnicianForm


# Custom 404 handler
def custom_404(request, exception):
    return render(request, 'equipment/404.html', status=404)


# Dashboard
def dashboard(request):
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


def equipment_list(request):
    equipment = Equipment.objects.select_related('category', 'manufacturer').all()
    categories = EquipmentCategory.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        equipment = equipment.filter(category_id=category_id)

    status = request.GET.get('status')
    if status:
        equipment = equipment.filter(status=status)

    context = {
        'equipment': equipment,
        'categories': categories,
    }
    return render(request, 'equipment/equipment_list.html', context)


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


def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save()
            messages.success(request, f'Оборудване {equipment.asset_number} е създадено успешно!')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm()

    return render(request, 'equipment/equipment_form.html', {'form': form, 'action': 'Добави'})


def equipment_update(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Оборудване {equipment.asset_number} е актуализирано успешно!')
            return redirect('equipment_detail', pk=equipment.pk)
    else:
        form = EquipmentForm(instance=equipment)

    return render(request, 'equipment/equipment_form.html',
                  {'form': form, 'action': 'Редактирай', 'equipment': equipment})


def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        asset_number = equipment.asset_number
        equipment.delete()
        messages.success(request, f'Equipment {asset_number} deleted successfully!')
        return redirect('equipment_list')

    return render(request, 'equipment/equipment_confirm_delete.html', {'equipment': equipment})


def manufacturer_list(request):
    manufacturers = Manufacturer.objects.all().order_by('name')
    context = {'manufacturers': manufacturers}
    return render(request, 'equipment/manufacturer_list.html', context)


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
            messages.success(request, f'Производител "{manufacturer.name}" е създаден успешно!')
            return redirect('manufacturer_detail', pk=manufacturer.pk)
    else:
        form = ManufacturerForm()

    return render(request, 'equipment/manufacturer_form.html', {'form': form, 'action': 'Създай'})


def manufacturer_update(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Производител "{manufacturer.name}" е актуализиран успешно!')
            return redirect('manufacturer_detail', pk=manufacturer.pk)
    else:
        form = ManufacturerForm(instance=manufacturer)

    return render(request, 'equipment/manufacturer_form.html',
                  {'form': form, 'action': 'Редактирай', 'manufacturer': manufacturer})


def manufacturer_delete(request, pk):
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if request.method == 'POST':
        name = manufacturer.name
        manufacturer.delete()
        messages.success(request, f'Производител "{name}" е изтрит успешно!')
        return redirect('manufacturer_list')

    return render(request, 'equipment/manufacturer_confirm_delete.html', {'manufacturer': manufacturer})


def category_list(request):
    categories = EquipmentCategory.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'equipment/category_list.html', context)


def category_detail(request, pk):
    category = get_object_or_404(EquipmentCategory, pk=pk)
    equipment_list = category.equipment.all()
    context = {
        'category': category,
        'equipment_list': equipment_list,
    }
    return render(request, 'equipment/category_detail.html', context)


def category_create(request):
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория "{category.name}" е създадена успешно!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = EquipmentCategoryForm()

    return render(request, 'equipment/category_form.html', {'form': form, 'action': 'Създай'})


# Category Update (UPDATE)
def category_update(request, pk):
    category = get_object_or_404(EquipmentCategory, pk=pk)
    if request.method == 'POST':
        form = EquipmentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Категория "{category.name}" е актуализирана успешно!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = EquipmentCategoryForm(instance=category)

    return render(request, 'equipment/category_form.html',
                  {'form': form, 'action': 'Редактирай', 'category': category})


def category_delete(request, pk):
    category = get_object_or_404(EquipmentCategory, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Категория "{name}" е изтрита успешно!')
        return redirect('category_list')

    return render(request, 'equipment/category_confirm_delete.html', {'category': category})


def department_list(request):
    departments = Department.objects.all().order_by('code')
    context = {'departments': departments}
    return render(request, 'equipment/department_list.html', context)


def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    locations = department.locations.all()
    technicians = department.technicians.filter(is_active=True)
    context = {
        'department': department,
        'locations': locations,
        'technicians': technicians,
    }
    return render(request, 'equipment/department_detail.html', context)


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Звено "{department.code}" е създадено успешно!')
            return redirect('department_detail', pk=department.pk)
    else:
        form = DepartmentForm()
    return render(request, 'equipment/department_form.html', {'form': form, 'action': 'Създай'})


def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'Звено "{department.code}" е актуализирано успешно!')
            return redirect('department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'equipment/department_form.html', {'form': form, 'action': 'Редактирай', 'department': department})


def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        code = department.code
        department.delete()
        messages.success(request, f'Звено "{code}" е изтрито успешно!')
        return redirect('department_list')
    return render(request, 'equipment/department_confirm_delete.html', {'department': department})


def location_list(request):
    locations = Location.objects.select_related('department').filter(is_active=True).order_by('category', 'floor', 'room_number')
    context = {'locations': locations}
    return render(request, 'equipment/location_list.html', context)


def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    equipment_list = location.equipment.all()
    context = {
        'location': location,
        'equipment_list': equipment_list,
    }
    return render(request, 'equipment/location_detail.html', context)


def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            messages.success(request, f'Локация "{location.code}" е създадена успешно!')
            return redirect('location_detail', pk=location.pk)
    else:
        form = LocationForm()
    return render(request, 'equipment/location_form.html', {'form': form, 'action': 'Създай'})


def location_update(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, f'Локация "{location.code}" е актуализирана успешно!')
            return redirect('location_detail', pk=location.pk)
    else:
        form = LocationForm(instance=location)
    return render(request, 'equipment/location_form.html', {'form': form, 'action': 'Редактирай', 'location': location})


def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        code = location.code
        location.delete()
        messages.success(request, f'Локация "{code}" е изтрита успешно!')
        return redirect('location_list')
    return render(request, 'equipment/location_confirm_delete.html', {'location': location})


def technician_list(request):
    technicians = Technician.objects.select_related('department').filter(is_active=True).order_by('last_name', 'first_name')
    context = {'technicians': technicians}
    return render(request, 'equipment/technician_list.html', context)


def technician_detail(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    context = {
        'technician': technician,
    }
    return render(request, 'equipment/technician_detail.html', context)


def technician_create(request):
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            technician = form.save()
            messages.success(request, f'Техник "{technician.get_full_name()}" е създаден успешно!')
            return redirect('technician_detail', pk=technician.pk)
    else:
        form = TechnicianForm()
    return render(request, 'equipment/technician_form.html', {'form': form, 'action': 'Създай'})


def technician_update(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        form = TechnicianForm(request.POST, instance=technician)
        if form.is_valid():
            form.save()
            messages.success(request, f'Техник "{technician.get_full_name()}" е актуализиран успешно!')
            return redirect('technician_detail', pk=technician.pk)
    else:
        form = TechnicianForm(instance=technician)
    return render(request, 'equipment/technician_form.html', {'form': form, 'action': 'Редактирай', 'technician': technician})


def technician_delete(request, pk):
    technician = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        name = technician.get_full_name()
        technician.delete()
        messages.success(request, f'Техник "{name}" е изтрит успешно!')
        return redirect('technician_list')
    return render(request, 'equipment/technician_confirm_delete.html', {'technician': technician})

