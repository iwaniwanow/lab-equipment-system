"""
Celery configuration for Equipment Management System
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('equipmentsystem')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-maintenance-due-daily': {
        'task': 'equipment.tasks.check_maintenance_due',
        'schedule': crontab(hour=8, minute=0),
    },
    'check-inspections-due-daily': {
        'task': 'equipment.tasks.check_inspections_due',
        'schedule': crontab(hour=8, minute=30),
    },
    'update-equipment-statuses': {
        'task': 'equipment.tasks.update_all_equipment_statuses',
        'schedule': crontab(hour=0, minute=0),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')

