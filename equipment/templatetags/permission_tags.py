from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Check if user belongs to a specific group
    Usage: {% if request.user|has_group:"Administrators" %}
    """
    if not user.is_authenticated:
        return False
    try:
        return user.groups.filter(name=group_name).exists()
    except:
        return False


@register.filter(name='has_any_group')
def has_any_group(user, group_names):
    """
    Check if user belongs to any of the groups
    Usage: {% if request.user|has_any_group:"Administrators,Managers" %}
    """
    if not user.is_authenticated:
        return False
    try:
        groups = [g.strip() for g in group_names.split(',')]
        return user.groups.filter(name__in=groups).exists()
    except:
        return False


@register.filter(name='has_perm')
def has_perm(user, perm):
    """
    Check if user has specific permission
    Usage: {% if request.user|has_perm:"equipment.add_equipment" %}
    """
    if not user.is_authenticated:
        return False
    return user.has_perm(perm)


@register.filter(name='can_add')
def can_add(user, model_name):
    """
    Check if user can add model
    Usage: {% if request.user|can_add:"equipment" %}
    """
    if not user.is_authenticated:
        return False
    return user.has_perm(f'equipment.add_{model_name}')


@register.filter(name='can_change')
def can_change(user, model_name):
    """
    Check if user can change model
    Usage: {% if request.user|can_change:"equipment" %}
    """
    if not user.is_authenticated:
        return False
    return user.has_perm(f'equipment.change_{model_name}')


@register.filter(name='can_delete')
def can_delete(user, model_name):
    """
    Check if user can delete model
    Usage: {% if request.user|can_delete:"equipment" %}
    """
    if not user.is_authenticated:
        return False
    return user.has_perm(f'equipment.delete_{model_name}')


@register.filter(name='user_role')
def user_role(user):
    """
    Get user role from profile
    Usage: {{ request.user|user_role }}
    """
    if not user.is_authenticated:
        return 'Anonymous'
    try:
        if hasattr(user, 'profile'):
            return user.profile.get_role_display()
        return 'No Role'
    except:
        return 'No Role'


@register.simple_tag
def user_can_edit(user):
    """
    Check if user can edit (Managers, Technicians, Administrators)
    Usage: {% user_can_edit request.user as can_edit %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__in=['Administrators', 'Managers', 'Technicians']).exists() or user.is_superuser


@register.simple_tag
def user_can_manage(user):
    """
    Check if user can manage (Managers, Administrators)
    Usage: {% user_can_manage request.user as can_manage %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name__in=['Administrators', 'Managers']).exists() or user.is_superuser


@register.simple_tag
def is_admin(user):
    """
    Check if user is administrator
    Usage: {% is_admin request.user as is_admin_user %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name='Administrators').exists() or user.is_superuser


@register.filter(name='can_modify_data')
def can_modify_data(user):
    """
    Проверява дали потребителят може да създава/редактира/изтрива данни
    Само admin и manager могат
    Usage: {% if request.user|can_modify_data %}
    """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if hasattr(user, 'profile'):
        return user.profile.role in ['admin', 'manager']
    return False


@register.filter(name='is_technician')
def is_technician(user):
    """
    Проверява дали потребителят е техник
    Usage: {% if request.user|is_technician %}
    """
    if not user.is_authenticated:
        return False
    if hasattr(user, 'profile'):
        return user.profile.role == 'technician'
    return False


