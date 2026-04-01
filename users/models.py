from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """
    Extended User model with additional fields
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('technician', 'Technician'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer',
        help_text="User role in the system"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
            )
        ],
        help_text="Contact phone number"
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Department name"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        """Return full name of the user"""
        return f"{self.first_name} {self.last_name}".strip() or self.username


class UserProfile(models.Model):
    """
    One-to-One relationship with CustomUser for additional profile information
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        help_text="Short biography"
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    
    birth_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date of birth"
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        help_text="Full address"
    )
    
    emergency_contact = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Emergency contact name and phone"
    )
    
    certifications = models.TextField(
        blank=True,
        null=True,
        help_text="Professional certifications (one per line)"
    )
    
    hire_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date of hire"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"Profile of {self.user.username}"

