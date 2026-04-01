from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin with extended fields
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_active', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active', 'department')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'department')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'department', 'email', 'first_name', 'last_name')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile Admin
    """
    list_display = ('user', 'hire_date', 'birth_date', 'created_at')
    list_filter = ('hire_date', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'bio')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('bio', 'avatar', 'birth_date', 'address', 'emergency_contact')
        }),
        ('Professional Information', {
            'fields': ('certifications', 'hire_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

