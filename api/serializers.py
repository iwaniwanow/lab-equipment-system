from rest_framework import serializers
from django.contrib.auth.models import User
from equipment.models import Equipment, Manufacturer, EquipmentCategory
from maintenance.models import MaintenanceRecord, MaintenanceType
from inspections.models import Inspection
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'full_name', 'role', 'phone', 'department', 
                  'bio', 'avatar', 'birth_date', 'certifications', 'hire_date']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.full_name


class ManufacturerSerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'website', 'contact_info', 'equipment_count']
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class EquipmentCategorySerializer(serializers.ModelSerializer):
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EquipmentCategory
        fields = ['id', 'name', 'description', 'equipment_count']
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class EquipmentListSerializer(serializers.ModelSerializer):
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    location_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Equipment
        fields = ['id', 'asset_number', 'name', 'manufacturer', 'manufacturer_name', 
                  'category', 'category_name', 'model', 'serial_number',
                  'location_name', 'status', 'status_display', 'commissioning_date']

    def get_location_name(self, obj):
        if obj.location:
            return str(obj.location)
        return obj.location_old if obj.location_old else None


class EquipmentDetailSerializer(serializers.ModelSerializer):
    manufacturer_details = ManufacturerSerializer(source='manufacturer', read_only=True)
    category_details = EquipmentCategorySerializer(source='category', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    maintenance_count = serializers.SerializerMethodField()
    inspection_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipment
        fields = '__all__'
    
    def get_maintenance_count(self, obj):
        return obj.maintenance_records.count()
    
    def get_inspection_count(self, obj):
        return obj.inspections.count()


class MaintenanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceType
        fields = ['id', 'name', 'description', 'period_months']


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    maintenance_type_name = serializers.CharField(source='maintenance_type.name', read_only=True)
    technician_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MaintenanceRecord
        fields = ['id', 'equipment', 'equipment_name', 'maintenance_type', 'maintenance_type_name',
                  'performed_date', 'next_due_date', 'technician', 'technician_name', 
                  'work_performed', 'parts_used', 'certificate_number', 'cost', 'currency']
        read_only_fields = ['next_due_date']
    
    def get_technician_name(self, obj):
        if obj.technician:
            return f"{obj.technician.first_name} {obj.technician.last_name}"
        return None


class InspectionSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    technician_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Inspection
        fields = ['id', 'equipment', 'equipment_name', 'inspection_type', 'inspection_date',
                  'next_inspection_date', 'technician', 'technician_name', 'status', 'status_display',
                  'findings', 'corrective_actions']
        read_only_fields = ['next_inspection_date']

    def get_technician_name(self, obj):
        if obj.technician:
            return f"{obj.technician.first_name} {obj.technician.last_name}"
        return None

