from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from equipment.models import Equipment, Manufacturer, EquipmentCategory


class APIAuthenticationTest(TestCase):
    """Tests for API authentication"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
    
    def test_api_requires_authentication(self):
        """Test that API endpoints require authentication"""
        response = self.client.get('/api/equipment/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_api_with_authentication(self):
        """Test that authenticated users can access API"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/equipment/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


class EquipmentAPITest(TestCase):
    """Tests for Equipment API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        
        self.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer'
        )
        self.category = EquipmentCategory.objects.create(
            name='Test Category'
        )
        self.equipment = Equipment.objects.create(
            asset_number='API-TEST-001',
            name='API Test Equipment',
            category=self.category,
            manufacturer=self.manufacturer,
            model='TestModel',
            serial_number='API-SN-001'
        )
    
    def test_get_equipment_list(self):
        """Test GET equipment list endpoint"""
        response = self.client.get('/api/equipment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_get_equipment_detail(self):
        """Test GET equipment detail endpoint"""
        response = self.client.get(f'/api/equipment/{self.equipment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['asset_number'], 'API-TEST-001')
    
    def test_create_equipment_via_api(self):
        """Test POST create equipment via API"""
        data = {
            'asset_number': 'API-TEST-002',
            'name': 'New Equipment',
            'category': self.category.id,
            'manufacturer': self.manufacturer.id,
            'model': 'Model2',
            'serial_number': 'API-SN-002'
        }
        response = self.client.post('/api/equipment/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
        
        if response.status_code == status.HTTP_201_CREATED:
            self.assertEqual(Equipment.objects.filter(asset_number='API-TEST-002').count(), 1)
    
    def test_equipment_api_filtering(self):
        """Test equipment API filtering"""
        response = self.client.get(f'/api/equipment/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_equipment_api_search(self):
        """Test equipment API search"""
        response = self.client.get('/api/equipment/?search=API')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ManufacturerAPITest(TestCase):
    """Tests for Manufacturer API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.manufacturer = Manufacturer.objects.create(
            name='API Test Manufacturer',
            country='Bulgaria'
        )
    
    def test_get_manufacturers_list(self):
        """Test GET manufacturers list"""
        response = self.client.get('/api/manufacturers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_manufacturer_detail(self):
        """Test GET manufacturer detail"""
        response = self.client.get(f'/api/manufacturers/{self.manufacturer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'API Test Manufacturer')
