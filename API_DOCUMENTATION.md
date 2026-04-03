# 📡 REST API Documentation
## Equipment Management System API

---

## 🌐 API Endpoints

API-то е достъпно на: **http://127.0.0.1:8000/api/**

### 📋 Browsable API Interface
Django REST Framework предоставя красив web interface за тестване на API-то:
- Отиди на http://127.0.0.1:8000/api/
- Ще видиш всички налични endpoints

---

## 🔑 Authentication

API-то изисква authentication. Има два начина:

### 1. Session Authentication (чрез браузър)
- Логни се в Django admin или през сайта
- След това API заявките ще работят автоматично в браузъра

### 2. Basic Authentication (чрез API клиенти)
```bash
# С curl:
curl -u username:password http://127.0.0.1:8000/api/equipment/

# С httpie:
http -a username:password http://127.0.0.1:8000/api/equipment/

# С Python requests:
import requests
response = requests.get(
    'http://127.0.0.1:8000/api/equipment/',
    auth=('username', 'password')
)
```

---

## 📚 API Endpoints List

### 1. Equipment API
**Base URL:** `/api/equipment/`

#### List All Equipment
```http
GET /api/equipment/
```
**Response:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "asset_number": "BAL-001",
            "name": "Analytical Balance Mettler Toledo XP205",
            "manufacturer": 1,
            "manufacturer_name": "Mettler Toledo",
            "category": 1,
            "category_name": "Balance",
            "model": "XP205",
            "serial_number": "B123456789",
            "status": "active",
            "status_display": "В експлоатация"
        }
    ]
}
```

#### Get Equipment Details
```http
GET /api/equipment/{id}/
```

#### Create Equipment
```http
POST /api/equipment/
Content-Type: application/json

{
    "asset_number": "BAL-002",
    "name": "Balance New",
    "manufacturer": 1,
    "category": 1,
    "model": "XP204",
    "serial_number": "B987654321",
    "location": 1
}
```

#### Update Equipment
```http
PUT /api/equipment/{id}/
PATCH /api/equipment/{id}/  (partial update)
```

#### Delete Equipment
```http
DELETE /api/equipment/{id}/
```

#### Custom Actions

**Get Maintenance History:**
```http
GET /api/equipment/{id}/maintenance_history/
```

**Get Inspection History:**
```http
GET /api/equipment/{id}/inspection_history/
```

**Get Equipment by Status:**
```http
GET /api/equipment/by_status/
```
Response:
```json
{
    "active": {
        "name": "В експлоатация",
        "count": 5
    },
    "pending_calibration": {
        "name": "Чака калибровка",
        "count": 2
    }
}
```

#### Filtering & Search

**Filter by status:**
```http
GET /api/equipment/?status=active
```

**Filter by category:**
```http
GET /api/equipment/?category=1
```

**Filter by manufacturer:**
```http
GET /api/equipment/?manufacturer=1
```

**Search by name/asset/serial:**
```http
GET /api/equipment/?search=balance
```

**Ordering:**
```http
GET /api/equipment/?ordering=asset_number
GET /api/equipment/?ordering=-name  (descending)
```

---

### 2. Manufacturers API
**Base URL:** `/api/manufacturers/`

```http
GET    /api/manufacturers/          # List all
GET    /api/manufacturers/{id}/     # Get details
POST   /api/manufacturers/          # Create
PUT    /api/manufacturers/{id}/     # Update
DELETE /api/manufacturers/{id}/     # Delete
```

**Response Example:**
```json
{
    "id": 1,
    "name": "Mettler Toledo",
    "country": "Switzerland",
    "website": "https://www.mt.com",
    "contact_info": "support@mt.com",
    "equipment_count": 5
}
```

**Search:**
```http
GET /api/manufacturers/?search=mettler
```

---

### 3. Equipment Categories API
**Base URL:** `/api/categories/`

```http
GET    /api/categories/          # List all
GET    /api/categories/{id}/     # Get details
POST   /api/categories/          # Create
PUT    /api/categories/{id}/     # Update
DELETE /api/categories/{id}/     # Delete
```

**Response Example:**
```json
{
    "id": 1,
    "name": "Balance",
    "description": "Analytical and precision balances",
    "equipment_count": 5
}
```

---

### 4. Maintenance Records API
**Base URL:** `/api/maintenance/`

```http
GET    /api/maintenance/          # List all
GET    /api/maintenance/{id}/     # Get details
POST   /api/maintenance/          # Create
PUT    /api/maintenance/{id}/     # Update
DELETE /api/maintenance/{id}/     # Delete
```

**Response Example:**
```json
{
    "id": 1,
    "equipment": 1,
    "equipment_name": "Analytical Balance XP205",
    "maintenance_type": 1,
    "maintenance_type_name": "Annual Calibration",
    "performed_date": "2026-01-15",
    "next_due_date": "2027-01-15",
    "technician": 1,
    "technician_name": "Ivan Ivanov",
    "work_performed": "Full calibration performed",
    "parts_used": "None",
    "certificate_number": "CAL-2026-001",
    "cost": "250.00",
    "currency": "BGN"
}
```

**Custom Actions:**

**Upcoming Maintenance (next 30 days):**
```http
GET /api/maintenance/upcoming/
```

**Overdue Maintenance:**
```http
GET /api/maintenance/overdue/
```

**Filtering:**
```http
GET /api/maintenance/?equipment=1
GET /api/maintenance/?maintenance_type=1
GET /api/maintenance/?technician=1
```

---

### 5. Maintenance Types API
**Base URL:** `/api/maintenance-types/`

```http
GET /api/maintenance-types/          # List all (read-only)
GET /api/maintenance-types/{id}/     # Get details (read-only)
```

**Response Example:**
```json
{
    "id": 1,
    "name": "Annual Calibration",
    "description": "Full calibration once per year",
    "period_months": 12
}
```

---

### 6. Inspections API
**Base URL:** `/api/inspections/`

```http
GET    /api/inspections/          # List all
GET    /api/inspections/{id}/     # Get details
POST   /api/inspections/          # Create
PUT    /api/inspections/{id}/     # Update
DELETE /api/inspections/{id}/     # Delete
```

**Response Example:**
```json
{
    "id": 1,
    "equipment": 1,
    "equipment_name": "Analytical Balance XP205",
    "inspection_date": "2026-04-01",
    "next_due_date": "2026-04-02",
    "inspector": 1,
    "inspector_name": "Maria Petrova",
    "result": "passed",
    "result_display": "Passed",
    "findings": "All checks passed",
    "corrective_actions": ""
}
```

**Custom Actions:**

**Failed Inspections:**
```http
GET /api/inspections/failed/
```

**Filtering:**
```http
GET /api/inspections/?equipment=1
GET /api/inspections/?result=failed
GET /api/inspections/?inspector=1
```

---

### 7. User Profiles API
**Base URL:** `/api/profiles/`

```http
GET /api/profiles/          # List all (read-only)
GET /api/profiles/{id}/     # Get details (read-only)
```

**Response Example:**
```json
{
    "id": 1,
    "user": 1,
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Admin User",
    "role": "admin",
    "phone": "+359888123456",
    "department": 1,
    "bio": "System administrator",
    "avatar": "/media/avatars/admin.jpg",
    "birth_date": "1990-01-01",
    "certifications": "ISO 9001 Auditor",
    "hire_date": "2020-01-01"
}
```

**Search:**
```http
GET /api/profiles/?search=admin
```

---

## 🧪 Testing API с Browsable Interface

### Стъпка 1: Отвори браузъра
```
http://127.0.0.1:8000/api/
```

### Стъпка 2: Логни се
Ако не си логнат, натисни **"Log in"** горе в дясно

### Стъпка 3: Browse Endpoints
Ще видиш списък с всички endpoints:
```
{
    "equipment": "http://127.0.0.1:8000/api/equipment/",
    "manufacturers": "http://127.0.0.1:8000/api/manufacturers/",
    "categories": "http://127.0.0.1:8000/api/categories/",
    "maintenance": "http://127.0.0.1:8000/api/maintenance/",
    "maintenance-types": "http://127.0.0.1:8000/api/maintenance-types/",
    "inspections": "http://127.0.0.1:8000/api/inspections/",
    "profiles": "http://127.0.0.1:8000/api/profiles/"
}
```

### Стъпка 4: Click на endpoint
Например: http://127.0.0.1:8000/api/equipment/

Ще видиш:
- Списък с данни (GET)
- Форма за създаване (POST) - долу на страницата
- Филтри - горе в дясно (Filter, Search)

### Стъпка 5: Тествай операции
**CREATE (POST):**
- Scroll down до формата
- Попълни полетата
- Натисни "POST"

**UPDATE (PUT/PATCH):**
- Отвори конкретен запис (напр. `/api/equipment/1/`)
- Промени данните във формата
- Натисни "PUT" или "PATCH"

**DELETE:**
- Отвори конкретен запис
- Scroll до края
- Натисни червения "DELETE" бутон

---

## 🔧 Testing API с curl (Command Line)

### GET Request
```bash
curl -u admin:password http://127.0.0.1:8000/api/equipment/
```

### POST Request (Create)
```bash
curl -u admin:password \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "asset_number": "TEST-001",
    "name": "Test Equipment",
    "manufacturer": 1,
    "category": 1,
    "model": "TEST-MODEL",
    "serial_number": "SN123456"
  }' \
  http://127.0.0.1:8000/api/equipment/
```

### PUT Request (Update)
```bash
curl -u admin:password \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "asset_number": "TEST-001",
    "name": "Updated Test Equipment",
    "manufacturer": 1,
    "category": 1,
    "model": "TEST-MODEL-V2",
    "serial_number": "SN123456"
  }' \
  http://127.0.0.1:8000/api/equipment/1/
```

### DELETE Request
```bash
curl -u admin:password \
  -X DELETE \
  http://127.0.0.1:8000/api/equipment/1/
```

---

## 🐍 Testing API с Python

### Installation
```bash
pip install requests
```

### Example Code
```python
import requests
from requests.auth import HTTPBasicAuth

# Configuration
BASE_URL = 'http://127.0.0.1:8000/api'
AUTH = HTTPBasicAuth('admin', 'password')

# List Equipment
response = requests.get(f'{BASE_URL}/equipment/', auth=AUTH)
print(response.json())

# Get Specific Equipment
response = requests.get(f'{BASE_URL}/equipment/1/', auth=AUTH)
equipment = response.json()
print(f"Equipment: {equipment['name']}")

# Create Equipment
new_equipment = {
    'asset_number': 'PY-TEST-001',
    'name': 'Python Test Equipment',
    'manufacturer': 1,
    'category': 1,
    'model': 'PY-MODEL',
    'serial_number': 'PYSN123456'
}
response = requests.post(
    f'{BASE_URL}/equipment/',
    json=new_equipment,
    auth=AUTH
)
print(f"Created: {response.status_code}")

# Update Equipment
update_data = {
    'name': 'Updated Python Test Equipment'
}
response = requests.patch(
    f'{BASE_URL}/equipment/1/',
    json=update_data,
    auth=AUTH
)
print(f"Updated: {response.status_code}")

# Delete Equipment
response = requests.delete(
    f'{BASE_URL}/equipment/1/',
    auth=AUTH
)
print(f"Deleted: {response.status_code}")

# Search Equipment
response = requests.get(
    f'{BASE_URL}/equipment/',
    params={'search': 'balance'},
    auth=AUTH
)
results = response.json()
print(f"Found {results['count']} items")

# Filter by Status
response = requests.get(
    f'{BASE_URL}/equipment/',
    params={'status': 'active'},
    auth=AUTH
)
print(f"Active equipment: {response.json()['count']}")

# Get Maintenance History for Equipment
response = requests.get(
    f'{BASE_URL}/equipment/1/maintenance_history/',
    auth=AUTH
)
history = response.json()
print(f"Maintenance records: {len(history)}")

# Get Upcoming Maintenance
response = requests.get(
    f'{BASE_URL}/maintenance/upcoming/',
    auth=AUTH
)
upcoming = response.json()
print(f"Upcoming maintenance: {len(upcoming)}")
```

---

## 📊 API Features Summary

### ✅ What's Available

1. **Full CRUD Operations**
   - Create, Read, Update, Delete for all major models
   
2. **Authentication & Permissions**
   - Session Authentication (for browser)
   - Basic Authentication (for API clients)
   - All endpoints require login
   
3. **Filtering**
   - Filter by status, category, manufacturer, etc.
   - Django Filter Backend integrated
   
4. **Search**
   - Full-text search on multiple fields
   - Search by name, asset_number, serial_number, etc.
   
5. **Ordering**
   - Sort by any field (ascending/descending)
   
6. **Pagination**
   - 20 items per page (configurable)
   - Next/Previous links
   
7. **Custom Actions**
   - Equipment: maintenance_history, inspection_history, by_status
   - Maintenance: upcoming, overdue
   - Inspections: failed
   
8. **Browsable API**
   - Beautiful web interface for testing
   - Interactive forms
   - Auto-generated documentation

---

## 🎯 Use Cases

### 1. Mobile App Integration
Можеш да използваш API-то за mobile app:
```javascript
// React Native / Expo example
fetch('http://yourserver.com/api/equipment/', {
  headers: {
    'Authorization': 'Basic ' + btoa('username:password')
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

### 2. External System Integration
Интеграция с други системи (ERP, LIMS, etc.):
```python
# Automatic sync from external system
def sync_equipment_from_erp():
    erp_data = get_equipment_from_erp()
    for item in erp_data:
        requests.post(
            'http://equipmentsystem.com/api/equipment/',
            json=item,
            auth=AUTH
        )
```

### 3. Automated Reporting
Генериране на автоматични доклади:
```python
# Daily maintenance report
def generate_daily_report():
    upcoming = requests.get(
        'http://127.0.0.1:8000/api/maintenance/upcoming/',
        auth=AUTH
    ).json()
    
    overdue = requests.get(
        'http://127.0.0.1:8000/api/maintenance/overdue/',
        auth=AUTH
    ).json()
    
    send_email_report(upcoming, overdue)
```

### 4. Data Analytics
Извличане на данни за анализ:
```python
# Get all equipment for analysis
import pandas as pd

response = requests.get(
    'http://127.0.0.1:8000/api/equipment/',
    auth=AUTH
)
df = pd.DataFrame(response.json()['results'])
print(df.describe())
```

---

## 🔒 Security Notes

1. **Always use HTTPS in production**
2. **Never hardcode credentials** - use environment variables
3. **Use token authentication** for production (JWT recommended)
4. **Rate limiting** - implement for production
5. **CORS** - configure for cross-origin requests

---

## 📝 Next Steps for Advanced

### To Add for Full Compliance:
1. **Token Authentication** (JWT)
2. **API Versioning** (/api/v1/)
3. **Rate Limiting**
4. **API Documentation** (Swagger/OpenAPI)
5. **WebSocket support** for real-time updates
6. **GraphQL endpoint** (optional advanced feature)

---

**Created:** 03.04.2026  
**Status:** ✅ Fully Functional  
**Testing:** http://127.0.0.1:8000/api/

