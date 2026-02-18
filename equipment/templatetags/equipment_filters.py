from django import template

register = template.Library()


@register.filter(name='status_badge')
def status_badge(status):
    """
    Custom template filter to return Bootstrap badge class based on equipment status.

    Usage in template:
    {{ equipment.status|status_badge }}

    Returns: Bootstrap badge class (success, warning, danger, secondary)
    """
    status_map = {
        'operational': 'success',
        'maintenance': 'warning',
        'calibration': 'danger',
        'out_of_service': 'secondary',
    }
    return status_map.get(status, 'secondary')


@register.filter(name='inspection_badge')
def inspection_badge(status):
    """
    Custom template filter to return Bootstrap badge class based on inspection status.

    Usage in template:
    {{ inspection.status|inspection_badge }}

    Returns: Bootstrap badge class (success, danger, warning)
    """
    status_map = {
        'passed': 'success',
        'failed': 'danger',
        'needs_attention': 'warning',
    }
    return status_map.get(status, 'secondary')


@register.filter(name='days_until')
def days_until(date_value):
    """
    Custom template filter to calculate days until a given date.

    Usage in template:
    {{ maintenance.next_due_date|days_until }}

    Returns: Integer (negative if overdue, positive if upcoming)
    """
    from datetime import date
    if not date_value:
        return None

    today = date.today()
    delta = date_value - today
    return delta.days


@register.filter(name='is_overdue')
def is_overdue(date_value):
    """
    Custom template filter to check if a date is overdue.

    Usage in template:
    {% if maintenance.next_due_date|is_overdue %}
        <span class="badge bg-danger">Overdue</span>
    {% endif %}

    Returns: Boolean
    """
    from datetime import date
    if not date_value:
        return False

    today = date.today()
    return date_value < today

