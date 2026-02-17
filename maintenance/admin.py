from django.contrib import admin
from .models import MaintenanceType, MaintenanceRecord

admin.site.register(MaintenanceType)
admin.site.register(MaintenanceRecord)
