from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from equipment.models import (
    Equipment, Manufacturer, EquipmentCategory,
    Department, Location, Technician
)
from users.models import UserProfile


class ManufacturerModelTest(TestCase):
    """Tests for Manufacturer model"""

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
            country='Bulgaria',
            website='https://test.com',
            contact_info='test@test.com'
        )

    def test_manufacturer_creation(self):
        """Test manufacturer is created correctly"""
        self.assertEqual(self.manufacturer.name, 'Test Manufacturer')
        self.assertEqual(self.manufacturer.country, 'Bulgaria')
        self.assertEqual(str(self.manufacturer), 'Test Manufacturer')

    def test_manufacturer_unique_name(self):
        """Test manufacturer name must be unique"""
        with self.assertRaises(Exception):
            Manufacturer.objects.create(
                name='Test Manufacturer',  # Duplicate
                country='Germany'
            )


class EquipmentCategoryModelTest(TestCase):
    """Tests for EquipmentCategory model"""

    def setUp(self):
        self.category = EquipmentCategory.objects.create(
            name='HPLC System',
            description='High Performance Liquid Chromatography'
        )

    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, 'HPLC System')
        self.assertEqual(str(self.category), 'HPLC System')

    def test_category_unique_name(self):
        """Test category name must be unique"""
        with self.assertRaises(Exception):
            EquipmentCategory.objects.create(
                name='HPLC System'  # Duplicate
            )


class EquipmentModelTest(TestCase):
    """Tests for Equipment model"""

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name='Agilent',
            country='USA'
        )
        self.category = EquipmentCategory.objects.create(
            name='HPLC'
        )
        self.department = Department.objects.create(
            code='QC',
            name='Quality Control',
            full_name='Quality Control Department'
        )
        self.location = Location.objects.create(
            code='A-1-101',
            category='A',
            floor=1,
            room_number='101',
            name='Lab 101',
            department=self.department
        )
        self.equipment = Equipment.objects.create(
            asset_number='TEST-001',
            name='Test HPLC',
            category=self.category,
            manufacturer=self.manufacturer,
            model='1200',
            serial_number='SN123456',
            location=self.location,
            commissioning_date=date.today()
        )

    def test_equipment_creation(self):
        """Test equipment is created correctly"""
        self.assertEqual(self.equipment.asset_number, 'TEST-001')
        self.assertEqual(self.equipment.name, 'Test HPLC')
        self.assertEqual(self.equipment.status, 'active')
        self.assertEqual(str(self.equipment), 'TEST-001 - Test HPLC')

    def test_equipment_asset_number_uppercase(self):
        """Test asset number validation (uppercase only)"""
        # Valid asset numbers
        valid_numbers = ['ABC-123', 'TEST-001', 'HP-2000']
        for num in valid_numbers:
            eq = Equipment(
                asset_number=num,
                name='Test',
                category=self.category,
                manufacturer=self.manufacturer,
                model='Test',
                serial_number=f'SN{num}'
            )
            try:
                eq.full_clean()  # Should not raise
            except Exception as e:
                self.fail(f"Valid asset number {num} raised exception: {e}")

    def test_equipment_unique_serial_number(self):
        """Test serial number must be unique"""
        with self.assertRaises(Exception):
            Equipment.objects.create(
                asset_number='TEST-002',
                name='Another HPLC',
                category=self.category,
                manufacturer=self.manufacturer,
                model='1200',
                serial_number='SN123456',  # Duplicate
                location=self.location
            )

    def test_equipment_status_choices(self):
        """Test equipment status choices"""
        valid_statuses = ['active', 'pending_validation', 'pending_calibration',
                         'pending_technical_review', 'pending_multiple',
                         'maintenance', 'out_of_service']
        for status in valid_statuses:
            self.equipment.status = status
            self.equipment.save()
            self.assertEqual(self.equipment.status, status)


class DepartmentModelTest(TestCase):
    """Tests for Department model"""

    def setUp(self):
        self.department = Department.objects.create(
            code='QC',
            name='Quality Control',
            full_name='Quality Control Department',
            manager='John Doe',
            is_active=True
        )

    def test_department_creation(self):
        """Test department is created correctly"""
        self.assertEqual(self.department.code, 'QC')
        self.assertEqual(self.department.name, 'Quality Control')
        self.assertTrue(self.department.is_active)
        self.assertEqual(str(self.department), 'QC - Quality Control')

    def test_department_unique_code(self):
        """Test department code must be unique"""
        with self.assertRaises(Exception):
            Department.objects.create(
                code='QC',  # Duplicate
                name='Another QC'
            )


class LocationModelTest(TestCase):
    """Tests for Location model"""

    def setUp(self):
        self.department = Department.objects.create(
            code='LAB',
            name='Laboratory'
        )
        self.location = Location.objects.create(
            code='A-1-101',
            category='A',
            floor=1,
            room_number='101',
            name='Clean Room 101',
            department=self.department,
            has_controlled_temperature=True,
            has_controlled_humidity=True
        )

    def test_location_creation(self):
        """Test location is created correctly"""
        self.assertEqual(self.location.code, 'A-1-101')
        self.assertEqual(self.location.category, 'A')
        self.assertEqual(self.location.floor, 1)
        self.assertTrue(self.location.has_controlled_temperature)
        self.assertEqual(str(self.location), 'A-1-101 - Clean Room 101')

    def test_location_category_choices(self):
        """Test location category choices (A, B, C, D, E)"""
        valid_categories = ['A', 'B', 'C', 'D', 'E']
        for cat in valid_categories:
            loc = Location.objects.create(
                code=f'CAT-{cat}-1-999',
                category=cat,
                floor=9,
                room_number='999',
                name=f'Test Room {cat}',
                department=self.department
            )
            self.assertEqual(loc.category, cat)


class TechnicianModelTest(TestCase):
    """Tests for Technician model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='tech1',
            email='tech1@test.com',
            password='testpass123'
        )
        self.department = Department.objects.create(
            code='TECH',
            name='Technical'
        )
        self.technician = Technician.objects.create(
            user=self.user,
            first_name='John',
            last_name='Smith',
            position='Senior Technician',
            specialization='metrology',
            phone='+359888123456',
            email='john@test.com',
            department=self.department,
            is_active=True
        )

    def test_technician_creation(self):
        """Test technician is created correctly"""
        self.assertEqual(self.technician.first_name, 'John')
        self.assertEqual(self.technician.last_name, 'Smith')
        self.assertEqual(self.technician.specialization, 'metrology')
        self.assertTrue(self.technician.is_active)
        # __str__ includes department code in parentheses
        self.assertIn('John Smith', str(self.technician))
        self.assertIn('Senior Technician', str(self.technician))

    def test_technician_specialization_choices(self):
        """Test technician specialization choices"""
        valid_specs = ['electrical', 'mechanical', 'it', 'metrology',
                      'quality_control', 'laboratory', 'hvac', 'safety',
                      'general', 'other']
        for spec in valid_specs:
            tech = Technician(
                first_name='Test',
                last_name='Tech',
                position='Technician',
                specialization=spec,
                department=self.department
            )
            try:
                tech.full_clean()
            except Exception as e:
                self.fail(f"Valid specialization {spec} raised exception: {e}")

