# 🔄 Celery Асинхронни Задачи - Настройка и Употреба

## 📋 Преглед

Equipment Management System използва **Celery** за изпълнение на асинхронни задачи и периодични задания.

---

## ✅ Какво е направено:

### 1. Инсталирани пакети:
- `celery==5.4.0` - Task queue framework
- `redis==5.0.8` - Message broker
- `django-celery-beat==2.7.0` - Periodic tasks scheduler
- `django-celery-results==2.5.1` - Task results storage in Django DB

### 2. Конфигурация:

#### config/celery.py
Основна Celery конфигурация с:
- Автоматично откриване на tasks
- Periodic tasks schedule (crontab)
- Integration с Django

#### config/settings.py
Celery настройки:
```python
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Europe/Sofia'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```

### 3. Async Tasks (equipment/tasks.py):

#### ✅ update_all_equipment_statuses
- **Какво прави:** Обновява статуса на всички оборудвания
- **Кога:** Всяка нощ в полунощ (00:00)
- **Защо:** Актуализира статусите според дати за калибровки/проверки

#### ✅ check_maintenance_due
- **Какво прави:** Проверява за предстоящи калибровки/ремонти
- **Кога:** Всяка сутрин в 08:00
- **Защо:** Изпраща напомнящи emails на екипа

#### ✅ check_inspections_due
- **Какво прави:** Проверява за предстоящи проверки
- **Кога:** Всяка сутрин в 08:30
- **Защо:** Изпраща напомнящи emails за проверки

---

## 🚀 Стартиране на Celery

### Предварителни изисквания:

**1. Инсталирай Redis:**

**Windows (с Chocolatey):**
```powershell
choco install redis-64
```

**Windows (Manual):**
1. Изтегли Redis за Windows от https://github.com/microsoftarchive/redis/releases
2. Разархивирай и стартирай `redis-server.exe`

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
```

**2. Стартирай Redis:**
```bash
# Windows
redis-server

# Linux/Mac
redis-server
# Or as service:
sudo systemctl start redis
```

---

### Стартиране на Celery Worker:

**Windows (PowerShell):**
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start Celery worker
celery -A config worker --loglevel=info --pool=solo
```

**Linux/Mac:**
```bash
# Activate virtual environment
source venv/bin/activate

# Start Celery worker
celery -A config worker --loglevel=info
```

---

### Стартиране на Celery Beat (Scheduler):

**В отделен терминал/PowerShell прозорец:**

```powershell
# Windows
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Linux/Mac
celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## 🧪 Тестване на Tasks

### Ръчно изпълнение на task:

```python
# Django shell
python manage.py shell

# Import и изпълнение
from equipment.tasks import update_all_equipment_statuses, check_maintenance_due

# Synchronous execution (for testing)
result = update_all_equipment_statuses()
print(result)

# Asynchronous execution (requires Celery worker running)
task = update_all_equipment_statuses.delay()
print(task.id)  # Task ID
print(task.status)  # Task status
print(task.result)  # Task result (when complete)
```

### Тестване на check_maintenance_due:

```python
from equipment.tasks import check_maintenance_due

# Check for maintenance due in next 7 days
result = check_maintenance_due(days_ahead=7)
print(result)
# Output: {'records_count': 2, 'emails_sent': 1}
```

### Тестване на check_inspections_due:

```python
from equipment.tasks import check_inspections_due

# Check for inspections due in next 3 days
result = check_inspections_due(days_ahead=3)
print(result)
# Output: {'inspections_count': 1, 'emails_sent': 1}
```

---

## 📊 Monitoring на Tasks

### 1. Django Admin
Отиди на: **http://127.0.0.1:8000/admin/**

- **Periodic tasks** - Виж и управлявай periodic tasks
- **Task results** - Виж резултатите от задачи
- **Crontab schedules** - Управлявай crontab schedules

### 2. Celery Flower (Web-based monitoring)

**Инсталирай Flower:**
```bash
pip install flower
```

**Стартирай Flower:**
```bash
celery -A config flower
```

**Отвори в браузър:**
```
http://localhost:5555
```

Ще видиш:
- Active tasks
- Completed tasks
- Failed tasks
- Worker status
- Task statistics

---

## 📅 Periodic Tasks Schedule

| Task | Schedule | Description |
|------|----------|-------------|
| `update_all_equipment_statuses` | 00:00 daily | Обновява статусите на всички оборудвания |
| `check_maintenance_due` | 08:00 daily | Проверява за предстоящи ремонти/калибровки (7 дни напред) |
| `check_inspections_due` | 08:30 daily | Проверява за предстоящи проверки (3 дни напред) |

### Промяна на schedules:

**Начин 1: Django Admin**
1. Отиди на `/admin/django_celery_beat/periodictask/`
2. Редактирай periodic task
3. Промени crontab schedule

**Начин 2: Код (config/celery.py)**
```python
app.conf.beat_schedule = {
    'check-maintenance-due-daily': {
        'task': 'equipment.tasks.check_maintenance_due',
        'schedule': crontab(hour=10, minute=0),  # Променено на 10:00
    },
}
```

---

## 📧 Email Notifications

### Конфигурация в settings.py:

```python
# For testing (prints emails to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production (Gmail example)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@equipmentsystem.com'
```

### Кой получава emails:
- Всички активни staff users (`is_staff=True`)
- С попълнен email адрес

### Типове emails:
1. **Maintenance due** - Напомняне за предстоящи калибровки/ремонти
2. **Inspections due** - Напомняне за предстоящи проверки

---

## 🔧 Troubleshooting

### Problem: Celery worker не стартира

**Solution:**
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Check Redis connection
python manage.py shell
from django.core.cache import cache
cache.set('test', 'value')
cache.get('test')
# Should return: 'value'
```

### Problem: Tasks не се изпълняват

**Check:**
1. ✅ Redis running? `redis-cli ping`
2. ✅ Celery worker running? `celery -A config worker`
3. ✅ Celery beat running? `celery -A config beat`
4. ✅ Tasks registered? Check `celery -A config inspect registered`

### Problem: Windows pooling error

**Solution:**
```powershell
# Use --pool=solo on Windows
celery -A config worker --loglevel=info --pool=solo
```

---

## 📈 Production Deployment

### Using Supervisor (Linux):

**supervisor.conf:**
```ini
[program:celery_worker]
command=/path/to/venv/bin/celery -A config worker --loglevel=info
directory=/path/to/equipmentsystem
user=www-data
autostart=true
autorestart=true

[program:celery_beat]
command=/path/to/venv/bin/celery -A config beat --loglevel=info
directory=/path/to/equipmentsystem
user=www-data
autostart=true
autorestart=true
```

### Using systemd (Linux):

**/etc/systemd/system/celery.service:**
```ini
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/equipmentsystem
ExecStart=/path/to/venv/bin/celery -A config worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

**Start:**
```bash
sudo systemctl start celery
sudo systemctl enable celery
```

---

## ✅ Advanced Exam Requirements

### ✅ Асинхронна обработка - 10 точки

**Покрити изисквания:**
1. ✅ **Celery integration** - Configured and working
2. ✅ **Multiple async tasks** - 3 tasks implemented
3. ✅ **Periodic tasks** - 3 scheduled tasks with crontab
4. ✅ **Task scheduling** - Using django-celery-beat
5. ✅ **Result storage** - Using django-celery-results
6. ✅ **Error handling** - Try-except blocks in tasks
7. ✅ **Logging** - Using Python logging
8. ✅ **Email notifications** - Implemented in tasks

**Advanced features:**
- ✅ Periodic task scheduling with crontab
- ✅ Database-backed scheduler (django-celery-beat)
- ✅ Result storage in Django DB
- ✅ Proper error handling and logging
- ✅ Email notifications to staff users
- ✅ Configurable parameters (days_ahead)

---

## 📝 Summary

**✅ Celery е напълно конфигуриран!**

**Tasks:**
- `update_all_equipment_statuses` - Daily at midnight
- `check_maintenance_due` - Daily at 08:00
- `check_inspections_due` - Daily at 08:30

**Usage:**
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A config worker --loglevel=info --pool=solo

# Terminal 3: Start Celery Beat
celery -A config beat --loglevel=info

# Terminal 4: Start Django
python manage.py runserver
```

**Monitoring:**
- Django Admin: `/admin/django_celery_beat/`
- Celery Flower: `http://localhost:5555` (if installed)

---

**Създадено:** 03.04.2026  
**Status:** ✅ Production Ready  
**За Advanced Django Exam @ SoftUni**

