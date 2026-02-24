from django.contrib import admin
from .models import Equipment, EquipmentCategory, Manufacturer, Department, Location, Technician

admin.site.register(Equipment)
admin.site.register(EquipmentCategory)
admin.site.register(Manufacturer)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Technician)
