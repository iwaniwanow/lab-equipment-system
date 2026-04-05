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

    def test_unapproved_user_cannot_login(self):
        """Test that unapproved users cannot login with specific message"""
        # Create unapproved user
        unapproved_user = User.objects.create_user(
            username='unapproved', 
            password='testpass123',
            email='unapproved@test.com'
        )
        # Profile should be created automatically with is_approved=False
        self.assertFalse(unapproved_user.profile.is_approved)
        
        # Try to login with CORRECT credentials
        response = self.client.post(
            reverse('users:login'), 
            {'username': 'unapproved', 'password': 'testpass123'},
            follow=True
        )
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # Should see specific message about waiting for approval
        self.assertContains(response, 'чака одобрение')
        
        # User should not be logged in
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_approved_user_can_login(self):
        """Test that approved users CAN login"""
        # Create approved user
        approved_user = User.objects.create_user(
            username='approved',
            password='testpass123',
            email='approved@test.com'
        )
        approved_user.profile.is_approved = True
        approved_user.profile.save()

        # Try to login
        response = self.client.post(
            reverse('users:login'),
            {'username': 'approved', 'password': 'testpass123'}
        )

        # Should redirect (successful login)
        self.assertEqual(response.status_code, 302)

    def test_superuser_can_login_without_approval(self):
        """Test that superusers can login even without approval"""
        # Create superuser without approval
        superuser = User.objects.create_superuser(
            username='superuser',
            password='adminpass',
            email='super@test.com'
        )
        # Explicitly set is_approved to False
        superuser.profile.is_approved = False
        superuser.profile.save()
        
        # Superuser should still be able to login
        response = self.client.post(
            reverse('users:login'),
            {'username': 'superuser', 'password': 'adminpass'}
        )
        
        # Should redirect (successful login)
        self.assertEqual(response.status_code, 302)
    
    def test_wrong_password_shows_generic_error(self):
        """Test that wrong password shows generic error, not approval message"""
        # Create unapproved user
        unapproved_user = User.objects.create_user(
            username='testuser',
            password='correctpass',
            email='test@test.com'
        )
        self.assertFalse(unapproved_user.profile.is_approved)
        
        # Try to login with WRONG password
        response = self.client.post(
            reverse('users:login'),
            {'username': 'testuser', 'password': 'wrongpass'},
            follow=True
        )
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # Should NOT see approval message
        self.assertNotContains(response, 'чака одобрение')
        
        # Should see generic invalid login message
        self.assertContains(response, 'правилно потребителско име и парола')
        
        # User should not be logged in
        self.assertFalse('_auth_user_id' in self.client.session)
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
