from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipmentViewSet, ManufacturerViewSet, EquipmentCategoryViewSet,
    MaintenanceRecordViewSet, MaintenanceTypeViewSet,
    InspectionViewSet, UserProfileViewSet
)

app_name = 'api'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'categories', EquipmentCategoryViewSet, basename='category')
router.register(r'maintenance', MaintenanceRecordViewSet, basename='maintenance')
router.register(r'maintenance-types', MaintenanceTypeViewSet, basename='maintenance-type')
router.register(r'inspections', InspectionViewSet, basename='inspection')
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]

