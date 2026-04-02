from django.contrib import admin
from .models import Equipment, EquipmentCategory, Manufacturer, Department, Location, Technician


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['asset_number', 'name', 'category', 'manufacturer', 'status']
    list_filter = ['status', 'category', 'manufacturer']
    search_fields = ['asset_number', 'name', 'serial_number']


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'website']
    search_fields = ['name', 'country']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'manager', 'is_active']
    list_filter = ['is_active']
    search_fields = ['code', 'name', 'manager']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'floor', 'room_number', 'department', 'is_active']
    list_filter = ['category', 'is_active', 'department']
    search_fields = ['code', 'name', 'room_number']


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'user', 'position', 'specialization', 'department', 'company', 'is_active']
    list_filter = ['is_active', 'specialization', 'department']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'company']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Връзка с потребител', {
            'fields': ('user',),
            'description': 'Свържете техника с потребителски акаунт (ако е вътрешен служител)'
        }),
        ('Основна информация', {
            'fields': ('first_name', 'last_name', 'position', 'specialization')
        }),
        ('Контакти', {
            'fields': ('phone', 'email')
        }),
        ('Организация', {
            'fields': ('department', 'company')
        }),
        ('Сертификация', {
            'fields': ('certification', 'certification_expiry')
        }),
        ('Друго', {
            'fields': ('notes', 'is_active', 'created_at', 'updated_at')
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Име'
