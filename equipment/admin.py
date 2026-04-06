from django.contrib import admin
from .models import Equipment, EquipmentCategory, Manufacturer, Department, Location, Technician, Tag, Document


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'equipment_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    filter_horizontal = ['equipment']

    def equipment_count(self, obj):
        return obj.equipment_count()
    equipment_count.short_description = 'Брой оборудване'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'document_type', 'uploaded_by', 'uploaded_at', 'equipment_count', 'is_active']
    list_filter = ['document_type', 'is_active', 'uploaded_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['equipment']
    readonly_fields = ['uploaded_at', 'uploaded_by']

    def equipment_count(self, obj):
        return obj.equipment_count()
    equipment_count.short_description = 'Брой оборудване'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

