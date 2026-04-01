# 🚀 QUICK START - ДЕН 1

## Какво направихме днес?

Създадохме пълна User Authentication система:
- ✅ CustomUser модел
- ✅ UserProfile (с avatar, bio, certifications)
- ✅ Registration, Login, Logout
- ✅ User profiles
- ✅ 5 User Groups с permissions

## 🎯 Следващи стъпки

### 1. Нова база данни (ПРЕПОРЪЧИТЕЛНО!)

В PostgreSQL създай нова база:
```sql
CREATE DATABASE equipmentsystem_advanced;
```

Или в PowerShell:
```powershell
psql -U postgres
CREATE DATABASE equipmentsystem_advanced;
\q
```

### 2. Update .env file

Промени в `.env`:
```env
DB_NAME=equipmentsystem_advanced
```

### 3. Migrations

```powershell
cd C:\Users\dbsupport2\PycharmProjects\equipmentsystem

# Delete old migrations (ако използваш нова БД)
python manage.py migrate --run-syncdb

# Migrate всичко
python manage.py migrate
```

### 4. Create Groups

```powershell
python manage.py create_groups
```

Резултат:
```
Created group: Administrators
Created group: Managers
Created group: Technicians
Created group: Operators
Created group: Viewers
✓ Successfully created all groups and permissions!
```

### 5. Create Superuser

```powershell
python manage.py createsuperuser
```

Примерни данни:
- Username: `admin`
- Email: `admin@lab.com`
- Password: `admin123`

### 6. Run Server

```powershell
python manage.py runserver
```

### 7. Test!

Отвори в browser:

**Registration:**
http://127.0.0.1:8000/users/register/

**Login:**
http://127.0.0.1:8000/users/login/

**Profile:**
http://127.0.0.1:8000/users/profile/
(след login)

**Admin:**
http://127.0.0.1:8000/admin/

## 📝 Тестване

### 1. Регистрация
- Отиди на `/users/register/`
- Попълни формата
- Провери validation errors
- Успешна регистрация → автоматичен redirect към login

### 2. Login
- Username и password
- Успешен login → redirect към dashboard

### 3. Profile
- Виж своя profile
- Кликни "Edit Profile"
- Качи avatar
- Добави bio, certifications
- Save changes

### 4. Admin
- Login като superuser
- Виж Users и User Profiles
- Виж Groups и Permissions
- Assign user to group

## 🎨 User Groups

Можеш да assignваш users към groups в Admin:

1. **Administrators** - Full access
2. **Managers** - Manage equipment, view records
3. **Technicians** - Perform maintenance/inspections
4. **Operators** - View equipment, create inspections
5. **Viewers** - Read-only access

## 🔧 Troubleshooting

### Грешка: "AUTH_USER_MODEL is not defined"
```powershell
# Delete all migrations and re-create
python manage.py migrate users zero
python manage.py makemigrations
python manage.py migrate
```

### Грешка: "table already exists"
```powershell
# Use fresh database
CREATE DATABASE equipmentsystem_advanced;
```

### Грешка: "avatar upload error"
```powershell
# Ensure media directory exists
New-Item -ItemType Directory -Force -Path "media\avatars"
```

## 📸 Screenshots

След регистрация трябва да видиш:
```
✓ Account created successfully for username! You can now log in.
```

След login:
```
✓ Welcome back, username!
```

След profile update:
```
✓ Your profile has been updated successfully!
```

## ⏭️ Какво следва утре (Ден 2)?

1. Създаване на `notifications` app
2. Създаване на `reports` app
3. Django REST Framework
4. API endpoints
5. Serializers
6. API permissions

---

**Статус:** ✅ День 1 ЗАВЪРШЕН  
**Време:** 1 април 2026  
**Commits:** 1/7  
**Next:** День 2 - REST API

