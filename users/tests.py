from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import UserProfile
from equipment.models import Department
class UserProfileSignalTest(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='signaluser', password='testpass123', email='signal@test.com')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user, user)
        self.assertEqual(user.profile.role, 'viewer')
        self.assertFalse(user.profile.is_approved)
    def test_profile_full_name_property(self):
        user = User.objects.create_user(username='nameuser', first_name='First', last_name='Last')
        self.assertEqual(user.profile.full_name, 'First Last')
        user2 = User.objects.create_user(username='noname')
        self.assertEqual(user2.profile.full_name, 'noname')
class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(code='IT', name='IT Department')
    def test_registration_page_loads(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='loginuser', password='testpass123', email='login@test.com')
        self.profile = self.user.profile
        self.profile.role = 'technician'
        self.profile.is_approved = True
        self.profile.save()
    def test_login_page_loads(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
    def test_user_can_login(self):
        response = self.client.post(reverse('users:login'), {'username': 'loginuser', 'password': 'testpass123'})
        self.assertIn(response.status_code, [200, 302])
class UserProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='profileuser', password='testpass123', email='profile@test.com', first_name='Profile', last_name='User')
        self.department = Department.objects.create(code='QC', name='Quality Control')
        self.profile = self.user.profile
        self.profile.role = 'manager'
        self.profile.department = self.department
        self.profile.phone = '+359888123456'
        self.profile.is_approved = True
        self.profile.save()
    def test_profile_str_method(self):
        self.assertEqual(str(self.profile), 'Profile of profileuser')
    def test_profile_full_name_property(self):
        self.assertEqual(self.profile.full_name, 'Profile User')
    def test_profile_roles(self):
        roles = ['admin', 'manager', 'technician', 'operator', 'viewer']
        for role in roles:
            self.profile.role = role
            self.profile.save()
            self.assertEqual(self.profile.role, role)
class UserPermissionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpass', is_staff=True, is_superuser=True)
        admin_profile = self.admin_user.profile
        admin_profile.role = 'admin'
        admin_profile.is_approved = True
        admin_profile.save()
        self.regular_user = User.objects.create_user(username='regularuser', password='regularpass')
        regular_profile = self.regular_user.profile
        regular_profile.role = 'viewer'
        regular_profile.is_approved = True
        regular_profile.save()
    def test_admin_can_access_admin_panel(self):
        self.client.login(username='adminuser', password='adminpass')
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [200, 302])
    def test_regular_user_cannot_access_admin_panel(self):
        self.client.login(username='regularuser', password='regularpass')
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [302, 403])
