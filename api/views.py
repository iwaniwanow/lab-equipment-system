from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from equipment.models import Equipment, Manufacturer, EquipmentCategory
from maintenance.models import MaintenanceRecord, MaintenanceType
from inspections.models import Inspection
from users.models import UserProfile
from .serializers import (
    EquipmentListSerializer, EquipmentDetailSerializer,
    ManufacturerSerializer, EquipmentCategorySerializer,
    MaintenanceRecordSerializer, MaintenanceTypeSerializer,
    InspectionSerializer, UserProfileSerializer
)
from .permissions import IsAuthenticatedOrReadOnly, IsAdminOrManagerOrReadOnly


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for equipment management
    Supports: list, retrieve, create, update, delete
    Filtering by status, category, manufacturer, location
    Search by name, asset_number, serial_number
    """
    queryset = Equipment.objects.select_related('manufacturer', 'category', 'location').all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'manufacturer', 'location']
    search_fields = ['name', 'asset_number', 'serial_number', 'model']
    ordering_fields = ['asset_number', 'name', 'commissioning_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return EquipmentListSerializer
        return EquipmentDetailSerializer
    
    @action(detail=True, methods=['get'])
    def maintenance_history(self, request, pk=None):
        """Get maintenance history for specific equipment"""
        equipment = self.get_object()
        maintenance_records = equipment.maintenance_records.all()
        serializer = MaintenanceRecordSerializer(maintenance_records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def inspection_history(self, request, pk=None):
        """Get inspection history for specific equipment"""
        equipment = self.get_object()
        inspections = equipment.inspections.all()
        serializer = InspectionSerializer(inspections, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get equipment grouped by status"""
        status_counts = {}
        for status_code, status_name in Equipment.STATUS_CHOICES:
            count = Equipment.objects.filter(status=status_code).count()
            status_counts[status_code] = {
                'name': status_name,
                'count': count
            }
        return Response(status_counts)


class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for manufacturers
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'country']
    ordering = ['name']


class EquipmentCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for equipment categories
    """
    queryset = EquipmentCategory.objects.all()
    serializer_class = EquipmentCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class MaintenanceRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for maintenance records
    """
    queryset = MaintenanceRecord.objects.select_related('equipment', 'maintenance_type', 'technician').all()
    serializer_class = MaintenanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['equipment', 'maintenance_type', 'technician']
    ordering_fields = ['performed_date', 'next_due_date']
    ordering = ['-performed_date']
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming maintenance due soon"""
        from datetime import date, timedelta
        upcoming_date = date.today() + timedelta(days=30)
        upcoming = self.queryset.filter(
            next_due_date__lte=upcoming_date,
            next_due_date__gte=date.today()
        )
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue maintenance"""
        from datetime import date
        overdue = self.queryset.filter(next_due_date__lt=date.today())
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)


class MaintenanceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for maintenance types (read-only)
    """
    queryset = MaintenanceType.objects.all()
    serializer_class = MaintenanceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class InspectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for inspections
    """
    queryset = Inspection.objects.select_related('equipment', 'inspection_type', 'technician').all()
    serializer_class = InspectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['equipment', 'status', 'technician', 'inspection_type']
    ordering_fields = ['inspection_date', 'next_inspection_date']
    ordering = ['-inspection_date']
    
    @action(detail=False, methods=['get'])
    def failed(self, request):
        """Get failed inspections"""
        failed = self.queryset.filter(status='failed')
        serializer = self.get_serializer(failed, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for user profiles (read-only)
    """
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'department', 'role']
