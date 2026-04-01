# 📋 CHECKLIST - Django Advanced Exam Project

## 🚀 QUICK START - ДЕН 1 ИНСТРУКЦИИ

### 1. Database Setup (ВАЖНО!)

**Опция А: Нова база данни (ПРЕПОРЪЧИТЕЛНО)**
```powershell
# В PostgreSQL command line или pgAdmin:
CREATE DATABASE equipmentsystem_advanced;
```

**Опция Б: Използване на съществуващата база**
⚠️ ВНИМАНИЕ: Ще загубиш всички Users! Направи бекъп първо!

```powershell
# Backup current database
pg_dump -U postgres equipmentsystem_db > backup_before_day1.sql
```

### 2. Apply Migrations

```powershell
cd C:\Users\dbsupport2\PycharmProjects\equipmentsystem

# Delete old database (if using new one)
python manage.py migrate users zero
python manage.py migrate --run-syncdb

# Apply all migrations
python manage.py migrate
```

### 3. Create Groups

```powershell
python manage.py create_groups
```

### 4. Create Superuser

```powershell
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (your choice)
```

### 5. Run Development Server

```powershell
python manage.py runserver
```

### 6. Test Pages

Visit these URLs:
- http://127.0.0.1:8000/users/register/ - Registration
- http://127.0.0.1:8000/users/login/ - Login
- http://127.0.0.1:8000/users/profile/ - Profile (after login)
- http://127.0.0.1:8000/admin/ - Admin panel

---

## ✅ ДЕН 1 - COMPLETED (1 April 2026)

### Изпълнено:
- [x] Users app created
- [x] CustomUser model with extended fields
- [x] UserProfile model (One-to-One)
- [x] 4 Forms with validations
- [x] 6 Views (3 CBVs, 3 FBVs)
- [x] 5 Templates (register, login, profile, profile_edit, user_detail)
- [x] 5 User Groups with permissions
- [x] Django Signals for auto-profile creation
- [x] Media files configuration
- [x] Git commit #1

### Models Created (2):
1. CustomUser - Extended AbstractUser
2. UserProfile - One-to-One profile

### Forms Created (4):
1. CustomUserCreationForm
2. CustomAuthenticationForm
3. UserUpdateForm
4. UserProfileUpdateForm

### Views Created (6):
1. RegisterView (CBV)
2. login_view (FBV)
3. logout_view (FBV)
4. ProfileView (CBV)
5. profile_edit_view (FBV)
6. UserDetailView (CBV)

### Templates Created (5):
1. users/register.html
2. users/login.html
3. users/profile.html
4. users/profile_edit.html
5. users/user_detail.html

---

## 📅 ДЕН 2 - TODO (2 April 2026)

### Цели:
- [ ] Create `notifications` app
- [ ] Create `reports` app
- [ ] Django REST Framework setup
- [ ] API endpoints (Equipment, Maintenance)
- [ ] API Serializers
- [ ] API Permissions
- [ ] Many-to-Many relationships
- [ ] Git commit #2

### Detailed Tasks:

#### 2.1 Notifications App
- [ ] Create app: `python manage.py startapp notifications`
- [ ] Model: Notification (user, title, message, read, created_at)
- [ ] Views: Notification list, mark as read, delete
- [ ] Template: notifications list
- [ ] WebSocket support (optional)

#### 2.2 Reports App
- [ ] Create app: `python manage.py startapp reports`
- [ ] Model: Report (title, report_type, generated_by, file, created_at)
- [ ] Views: Generate report, download report
- [ ] Report types: Equipment summary, Maintenance schedule, etc.

#### 2.3 Django REST Framework
- [ ] Install: `pip install djangorestframework`
- [ ] Add to INSTALLED_APPS
- [ ] Create serializers for:
  - Equipment
  - Maintenance
  - Inspection
  - CustomUser
- [ ] API Views (ViewSets):
  - EquipmentViewSet
  - MaintenanceViewSet
  - InspectionViewSet
- [ ] URLs: `/api/equipment/`, `/api/maintenance/`, etc.
- [ ] Permissions: IsAuthenticated, custom permissions

#### 2.4 Many-to-Many Relationships
- [ ] Add M2M to existing models
- [ ] Example: Equipment <-> Tags
- [ ] Example: Maintenance <-> Parts

---

## 📅 ДЕН 3 - PLAN (3 April 2026)

### Цели:
- [ ] Create remaining forms (need 7 total, have 4)
- [ ] Custom validators
- [ ] File upload functionality
- [ ] Confirmation pages for delete
- [ ] Enhanced error messages
- [ ] Git commit #3

### Forms to Create (3 more):
5. [ ] Equipment Create/Edit Form
6. [ ] Maintenance Record Form
7. [ ] Inspection Form

---

## 📅 ДЕН 4 - PLAN (4 April 2026)

### Цели:
- [ ] Convert all FBVs to CBVs (90% CBVs)
- [ ] Create remaining templates (need 15 total, have 5)
- [ ] Custom template filters
- [ ] Custom template tags
- [ ] Custom error pages (500, 403)
- [ ] Bootstrap responsive design improvements
- [ ] Git commit #4

### Templates to Create (10 more):
- [ ] Dashboard (updated)
- [ ] Equipment list/detail
- [ ] Maintenance list/detail
- [ ] Inspection list/detail
- [ ] Notifications list
- [ ] Reports list
- [ ] API documentation page
- [ ] 500 error page
- [ ] 403 error page
- [ ] About page

---

## 📅 ДЕН 5 - PLAN (5 April 2026)

### Цели:
- [ ] Celery setup
- [ ] Background tasks
- [ ] Periodic tasks
- [ ] Email notifications
- [ ] Advanced security
- [ ] Git commit #5

### Celery Tasks:
- [ ] Send email on maintenance due
- [ ] Generate reports asynchronously
- [ ] Clean old notifications
- [ ] Backup database

---

## 📅 ДЕН 6 - PLAN (6 April 2026)

### Цели:
- [ ] PostgreSQL setup for production
- [ ] Write 15+ tests
- [ ] Documentation in README
- [ ] Code cleanup
- [ ] Git commit #6

### Tests to Write (15+):
- [ ] Model tests (CustomUser, Equipment)
- [ ] View tests (Registration, Login)
- [ ] Form tests (Validation)
- [ ] API tests (Endpoints)
- [ ] Permission tests
- [ ] Signal tests

---

## 📅 ДЕН 7 - PLAN (7 April 2026)

### Цели:
- [ ] AWS deployment
- [ ] Environment variables
- [ ] Static/Media on S3
- [ ] Production settings
- [ ] Final testing
- [ ] Git commit #7
- [ ] Submit to SoftUni

### Deployment Checklist:
- [ ] Create AWS account (student)
- [ ] Setup EC2 or Elastic Beanstalk
- [ ] Configure PostgreSQL (RDS)
- [ ] Setup S3 for static/media
- [ ] Environment variables
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS
- [ ] SSL certificate
- [ ] Final testing
- [ ] Submit GitHub link

---

## 📊 OVERALL PROGRESS

### Requirements Checklist:

#### Core Requirements:
- [x] Public section (anonymous users)
- [x] Private section (authenticated users)
- [x] User registration ✅
- [x] User login ✅
- [x] User logout ✅
- [x] 2+ user groups ✅ (5 groups)
- [x] Extended User model ✅

#### Technical Stack:
- [x] Django 6.0.2 ✅
- [ ] 5+ Django apps (4/5 - need 1 more)
  - [x] equipment
  - [x] inspections
  - [x] maintenance
  - [x] users
  - [ ] notifications OR reports (Day 2)
- [x] 5+ database models ✅ (10+ models)
- [x] 2+ M2O relationships ✅
- [ ] 2+ M2M relationships (Day 2)

#### Forms and Validations:
- [ ] 7+ forms (4/7) ✅ (need 3 more - Day 3)
- [x] User-friendly error messages ✅
- [x] Custom validators ✅
- [x] Read-only fields ✅
- [ ] Confirmation pages (Day 3)

#### Views and APIs:
- [ ] 90% CBVs (50% currently - Day 4)
- [ ] 1+ RESTful API (Day 2)
- [ ] Serializers (Day 2)
- [ ] API permissions (Day 2)

#### Templates:
- [ ] 15+ templates (5/15 - Day 4)
- [ ] 10+ dynamic data templates (5/10)
- [ ] Full CRUD for 3+ models ✅
- [ ] Custom filters/tags (Day 4)
- [ ] Custom error pages (Day 4)
- [x] Base template ✅
- [x] Template inheritance ✅
- [x] Bootstrap responsive ✅

#### Additional Requirements:
- [ ] Asynchronous tasks (Day 5)
- [x] Security (CSRF, XSS) ✅
- [x] Environment variables ✅
- [x] PostgreSQL ✅
- [x] Media/static files ✅
- [ ] 15+ tests (Day 6)
- [ ] Deployment (Day 7)
- [ ] 7 commits on 7 days (1/7)

#### Documentation:
- [x] README (partial)
- [ ] Setup instructions (Day 6)
- [ ] Deployment docs (Day 7)

#### Code Quality:
- [x] OOP principles ✅
- [x] Clean code ✅
- [x] Exception handling ✅
- [x] Good naming ✅

---

## 🎯 SCORING ESTIMATE

| Criterion | Max Points | Current | Target |
|-----------|------------|---------|--------|
| Originality | 10 | 8 | 10 |
| Database Design | 5 | 5 | 5 |
| User Model & Auth | 5 | 5 | 5 |
| Forms & Validation | 5 | 3 | 5 |
| Views Implementation | 10 | 5 | 10 |
| Pages | 10 | 4 | 10 |
| Async Processing | 10 | 0 | 10 |
| RESTful APIs | 10 | 0 | 10 |
| Deployment | 10 | 0 | 10 |
| Tests | 5 | 0 | 5 |
| Security & Advanced | 10 | 6 | 10 |
| Documentation | 4 | 2 | 4 |
| Version Control | 3 | 0.4 | 3 |
| Code Quality | 3 | 2.5 | 3 |
| **TOTAL** | **100** | **40.9** | **100** |

---

## 📝 NOTES

### Environment Variables (.env):
```env
# Database
DB_NAME=equipmentsystem_advanced
DB_USER=postgres
DB_PASSWORD=iwaniwanow
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (for Day 5)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS (for Day 7)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### Useful Commands:
```powershell
# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create groups
python manage.py create_groups

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Run Celery (Day 5)
celery -A config worker -l info
```

---

**Last Updated:** 1 April 2026  
**Status:** Day 1 COMPLETED ✅  
**Next:** Day 2 - Apps & REST API

