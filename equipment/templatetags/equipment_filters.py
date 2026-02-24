from django import template

register = template.Library()


@register.filter(name='status_badge')
def status_badge(status):
    status_map = {
        'operational': 'success',
        'maintenance': 'warning',
        'calibration': 'danger',
        'out_of_service': 'secondary',
    }
    return status_map.get(status, 'secondary')


@register.filter(name='inspection_badge')
def inspection_badge(status):
    status_map = {
        'passed': 'success',
        'failed': 'danger',
        'needs_attention': 'warning',
    }
    return status_map.get(status, 'secondary')


@register.filter(name='days_until')
def days_until(date_value):
    from datetime import date
    if not date_value:
        return None

    today = date.today()
    delta = date_value - today
    return delta.days


@register.filter(name='is_overdue')
def is_overdue(date_value):
    from datetime import date
    if not date_value:
        return False

    today = date.today()
    return date_value < today

