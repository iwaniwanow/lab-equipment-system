from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from equipment.models import Equipment, Manufacturer, EquipmentCategory, Department, Technician
from inspections.models import InspectionType, Inspection


class InspectionTypeModelTest(TestCase):
    """Tests for InspectionType model"""

    def setUp(self):
        self.inspection_type = InspectionType.objects.create(
            name='Daily Suitability Check',
            category='suitability_check',
            frequency='daily',
            description='Daily check of equipment suitability',
            checklist='Check 1, Check 2, Check 3'
        )

    def test_inspection_type_creation(self):
        """Test inspection type is created correctly"""
        self.assertEqual(self.inspection_type.name, 'Daily Suitability Check')
        self.assertEqual(self.inspection_type.frequency, 'daily')
        self.assertEqual(str(self.inspection_type), 'Daily Suitability Check (Дневна)')

    def test_inspection_type_frequency_days(self):
        """Test get_frequency_days method"""
        self.assertEqual(self.inspection_type.get_frequency_days(), 1)

        weekly = InspectionType.objects.create(
            name='Weekly Check',
            frequency='weekly',
            description='Weekly check'
        )
        self.assertEqual(weekly.get_frequency_days(), 7)

        monthly = InspectionType.objects.create(
            name='Monthly Check',
            frequency='monthly',
            description='Monthly check'
        )
        self.assertEqual(monthly.get_frequency_days(), 30)

    def test_inspection_type_category_choices(self):
        """Test inspection type category choices"""
        valid_categories = ['technical_review', 'suitability_check']
        for cat in valid_categories:
            it = InspectionType.objects.create(
                name=f'Test {cat}',
                category=cat,
                frequency='daily',
                description='Test description',
                checklist='Check 1, Check 2'
            )
            self.assertEqual(it.category, cat)


class InspectionModelTest(TestCase):
    """Tests for Inspection model"""

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
        self.inspection_type = InspectionType.objects.create(
            name='Daily Check',
            category='suitability_check',
            frequency='daily'
        )
        self.department = Department.objects.create(
            code='LAB',
            name='Laboratory'
        )
        self.user = User.objects.create_user(username='tech1')
        self.technician = Technician.objects.create(
            user=self.user,
            first_name='Jane',
            last_name='Smith',
            position='Inspector',
            department=self.department
        )
        self.inspection = Inspection.objects.create(
            equipment=self.equipment,
            inspection_type=self.inspection_type,
            inspection_date=date.today(),
            status='passed',
            technician=self.technician,
            findings='All checks passed'
        )

    def test_inspection_creation(self):
        """Test inspection is created correctly"""
        self.assertEqual(self.inspection.equipment, self.equipment)
        self.assertEqual(self.inspection.inspection_type, self.inspection_type)
        self.assertEqual(self.inspection.status, 'passed')
        self.assertIsNotNone(self.inspection.next_inspection_date)

    def test_next_inspection_date_calculation(self):
        """Test automatic calculation of next inspection date"""
        expected_next_date = date.today() + timedelta(days=1)
        self.assertEqual(self.inspection.next_inspection_date, expected_next_date)

    def test_inspection_status_choices(self):
        """Test inspection status choices"""
        valid_statuses = ['passed', 'failed', 'needs_attention']
        for status in valid_statuses:
            self.inspection.status = status
            self.inspection.save()
            self.assertEqual(self.inspection.status, status)

