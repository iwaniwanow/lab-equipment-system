from django.contrib import admin
from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import UserProfile
from equipment.models import Technician


class CustomAdminSite(admin.AdminSite):
    site_header = "Система за лабораторно оборудване - Администрация"
    site_title = "Админ панел"
    index_title = "Табло за управление"

    def index(self, request, extra_context=None):
        """Custom admin index with statistics"""
        extra_context = extra_context or {}

        # Статистика за потребители
        extra_context['pending_users'] = UserProfile.objects.filter(is_approved=False).count()
        extra_context['approved_users'] = UserProfile.objects.filter(is_approved=True).count()
        extra_context['total_users'] = User.objects.count()

        # Статистика за техници
        extra_context['total_technicians'] = Technician.objects.filter(is_active=True).count()

        return super().index(request, extra_context)


# Създаваме custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

