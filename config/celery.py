"""
Celery configuration for Equipment Management System
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create Celery app
app = Celery('equipmentsystem')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed Django apps
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'check-maintenance-due-daily': {
        'task': 'equipment.tasks.check_maintenance_due',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8:00 AM
    },
    'check-inspections-due-daily': {
        'task': 'equipment.tasks.check_inspections_due',
        'schedule': crontab(hour=8, minute=30),  # Every day at 8:30 AM
    },
    'update-equipment-statuses': {
        'task': 'equipment.tasks.update_all_equipment_statuses',
        'schedule': crontab(hour=0, minute=0),  # Every day at midnight
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')

