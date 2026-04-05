from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task(name='equipment.tasks.update_all_equipment_statuses')
def update_all_equipment_statuses():
    from equipment.models import Equipment
    logger.info('Starting bulk equipment status update')
    updated_count = 0
    for equipment in Equipment.objects.all():
        try:
            equipment.update_status()
            updated_count += 1
        except Exception as e:
            logger.error(f'Error updating status for {equipment.asset_number}: {e}')
    logger.info(f'Updated {updated_count} equipment statuses')
    return {'total': Equipment.objects.count(), 'updated': updated_count}

@shared_task(name='equipment.tasks.check_maintenance_due')
def check_maintenance_due(days_ahead=7):
    from maintenance.models import MaintenanceRecord
    from django.contrib.auth.models import User
    logger.info(f'Checking maintenance due in next {days_ahead} days')
    today = timezone.now().date()
    future_date = today + timedelta(days=days_ahead)
    due_soon = MaintenanceRecord.objects.filter(
        next_due_date__gte=today,
        next_due_date__lte=future_date
    ).select_related('equipment', 'maintenance_type', 'technician')
    if not due_soon.exists():
        logger.info('No maintenance due soon')
        return {'count': 0}
    sent_count = 0
    for record in due_soon:
        subject = f'��������� ������: {record.equipment.asset_number}'
        message = f'���������� {record.equipment.name} ������� {record.maintenance_type.name} �� {record.next_due_date}'
        recipients = User.objects.filter(is_staff=True, is_active=True, email__isnull=False).exclude(email='').values_list('email', flat=True)
        if recipients:
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(recipients), fail_silently=False)
                sent_count += 1
            except Exception as e:
                logger.error(f'Error sending email: {e}')
    return {'records_count': due_soon.count(), 'emails_sent': sent_count}

@shared_task(name='equipment.tasks.check_inspections_due')
def check_inspections_due(days_ahead=3):
    from inspections.models import Inspection
    from django.contrib.auth.models import User
    logger.info(f'Checking inspections due in next {days_ahead} days')
    today = timezone.now().date()
    future_date = today + timedelta(days=days_ahead)
    due_soon = Inspection.objects.filter(
        next_inspection_date__gte=today,
        next_inspection_date__lte=future_date
    ).select_related('equipment', 'inspection_type')
    if not due_soon.exists():
        return {'count': 0}
    sent_count = 0
    for inspection in due_soon:
        subject = f'Предстояща инспекция: {inspection.equipment.asset_number}'
        message = f'Оборудване {inspection.equipment.name} изисква {inspection.inspection_type.name} до {inspection.next_inspection_date}'
        recipients = User.objects.filter(is_staff=True, is_active=True, email__isnull=False).exclude(email='').values_list('email', flat=True)
        if recipients:
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(recipients), fail_silently=False)
                sent_count += 1
            except Exception as e:
                logger.error(f'Error sending email: {e}')
    return {'inspections_count': due_soon.count(), 'emails_sent': sent_count}
