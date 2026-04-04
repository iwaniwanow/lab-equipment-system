from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from equipment.models import Equipment, Manufacturer, EquipmentCategory, Department, Technician
from maintenance.models import MaintenanceType, MaintenanceRecord


class MaintenanceTypeModelTest(TestCase):
    """Tests for MaintenanceType model"""
    
    def setUp(self):
        self.maintenance_type = MaintenanceType.objects.create(
            name='Annual Calibration',
            type='calibration',
            period_months=12,
            description='Annual calibration of equipment'
        )
    
    def test_maintenance_type_creation(self):
        """Test maintenance type is created correctly"""
        self.assertEqual(self.maintenance_type.name, 'Annual Calibration')
        self.assertEqual(self.maintenance_type.type, 'calibration')
        self.assertEqual(self.maintenance_type.period_months, 12)
        self.assertEqual(str(self.maintenance_type), 'Annual Calibration (Калибровка)')
    
    def test_maintenance_type_choices(self):
        """Test maintenance type choices"""
        valid_types = ['calibration', 'validation', 'technical_service', 'repair']
        for mtype in valid_types:
            mt = MaintenanceType(
                name=f'Test {mtype}',
                type=mtype,
                period_months=12,
                description='Test'
            )
            try:
                mt.full_clean()
            except Exception as e:
                self.fail(f"Valid type {mtype} raised exception: {e}")


class MaintenanceRecordModelTest(TestCase):
    """Tests for MaintenanceRecord model"""
    
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name='Test Mfr')
        self.category = EquipmentCategory.objects.create(name='Test Cat')
        self.equipment = Equipment.objects.create(
            asset_number='TEST-001',
            name='Test Equipment',
            category=self.category,
            manufacturer=self.manufacturer,
            model='Model1',
            serial_number='SN001'
        )
        self.maintenance_type = MaintenanceType.objects.create(
            name='Annual Calibration',
            type='calibration',
            period_months=12
        )
        self.department = Department.objects.create(
            code='TECH',
            name='Technical'
        )
        self.user = User.objects.create_user(username='tech1')
        self.technician = Technician.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            position='Technician',
            department=self.department
        )
        self.maintenance_record = MaintenanceRecord.objects.create(
            equipment=self.equipment,
            maintenance_type=self.maintenance_type,
            performed_date=date.today(),
            technician=self.technician,
            result='passed',
            work_performed='Calibration performed successfully',
            cost=250.00,
            currency='BGN'
        )
    
    def test_maintenance_record_creation(self):
        """Test maintenance record is created correctly"""
        self.assertEqual(self.maintenance_record.equipment, self.equipment)
        self.assertEqual(self.maintenance_record.maintenance_type, self.maintenance_type)
        self.assertEqual(self.maintenance_record.result, 'passed')
        self.assertIsNotNone(self.maintenance_record.next_due_date)
    
    def test_next_due_date_calculation(self):
        """Test automatic calculation of next due date"""
        expected_next_date = date.today() + relativedelta(months=12)
        self.assertEqual(self.maintenance_record.next_due_date, expected_next_date)
    
    def test_maintenance_record_result_choices(self):
        """Test maintenance record result choices"""
        valid_results = ['passed', 'failed', 'conditional']
        for result in valid_results:
            self.maintenance_record.result = result
            self.maintenance_record.save()
            self.assertEqual(self.maintenance_record.result, result)
    
    def test_maintenance_record_currency_choices(self):
        """Test maintenance record currency choices"""
        valid_currencies = ['BGN', 'EUR']
        for currency in valid_currencies:
            self.maintenance_record.currency = currency
            self.maintenance_record.save()
            self.assertEqual(self.maintenance_record.currency, currency)

