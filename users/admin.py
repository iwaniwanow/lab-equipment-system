from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('role', 'phone', 'department', 'is_approved', 'bio', 'avatar', 'birth_date', 'address', 'emergency_contact', 'certifications', 'hire_date')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'get_approved', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'profile__role', 'profile__is_approved')
    
    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return '-'
    get_role.short_description = 'Role'
    
    def get_approved(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.is_approved
        return False
    get_approved.short_description = 'Approved'
    get_approved.boolean = True


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_approved', 'phone', 'department', 'hire_date', 'created_at')
    list_filter = ('role', 'is_approved', 'hire_date', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'department')
    actions = ['approve_users', 'disapprove_users']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Approval Status', {
            'fields': ('is_approved',),
            'classes': ('wide',),
            'description': 'User must be approved before they can login'
        }),
        ('Role & Contact', {
            'fields': ('role', 'phone', 'department')
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
    
    def approve_users(self, request, queryset):
        """Одобри избраните потребители и създай Technician профил ако е необходимо"""
        from equipment.models import Technician
        
        updated = 0
        technicians_created = 0
        
        for profile in queryset:
            if not profile.is_approved:
                profile.is_approved = True
                profile.save()
                updated += 1
                
                # Ако ролята е 'technician' и няма Technician профил, създай
                if profile.role == 'technician' and not hasattr(profile.user, 'technician_profile'):
                    Technician.objects.create(
                        user=profile.user,
                        first_name=profile.user.first_name,
                        last_name=profile.user.last_name,
                        email=profile.user.email,
                        phone=profile.phone or '',
                        department=profile.department,
                        specialization='general',
                        is_active=True
                    )
                    technicians_created += 1
        
        if technicians_created > 0:
            self.message_user(request, f'{updated} потребители одобрени. {technicians_created} Technician профили създадени.')
        else:
            self.message_user(request, f'{updated} потребители одобрени успешно.')
    approve_users.short_description = "✓ Одобри избраните потребители"
    
    def disapprove_users(self, request, queryset):
        """Disapprove selected users"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} потребители отхвърлени.')
    disapprove_users.short_description = "✗ Отхвърли избраните потребители"

