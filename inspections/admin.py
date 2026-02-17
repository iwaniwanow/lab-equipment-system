from django.contrib import admin
from .models import Inspection, InspectionType

admin.site.register(Inspection)
admin.site.register(InspectionType)
