# Laboratory Equipment Management System

A comprehensive Django-based web application for managing laboratory equipment, maintenance records, and inspections in pharmaceutical and analytical laboratories compliant with GMP/ISO standards.

## 📋 Features

### Equipment Management
- Complete CRUD operations for laboratory equipment
- Equipment categorization (pH meters, balances, spectrophotometers, etc.)
- Manufacturer database management
- Asset number tracking with validation
- Serial number tracking
- Location management
- **Automatic status calculation** based on maintenance and inspection due dates

### Maintenance Management
- Maintenance record tracking (calibration, validation, technical service)
- **Automatic calculation of next due dates** based on maintenance type period
- Support for:
  - **Calibration** (annual, semi-annual, quarterly)
  - **OQ/PV Validation** (Operational Qualification, Performance Validation)
  - **Technical Service** (preventive maintenance)
  - **Repairs** (corrective maintenance)
- Certificate/protocol number tracking
- Cost tracking
- Many-to-Many relationship: Equipment can have multiple required maintenance types

### Inspection Management
- Inspection record tracking with configurable frequencies
- **Automatic calculation of next inspection dates**
- Support for:
  - Daily, Weekly, Monthly inspections
  - Quarterly (3 months), Bi-annual (6 months), Annual inspections
- Inspection status tracking (Passed, Failed, Needs Attention)
- Corrective actions documentation
- Customizable inspection checklists

### Reference Data Management
- **Manufacturers**: Database of equipment manufacturers with contact information
- **Equipment Categories**: Customizable equipment categories
- **Maintenance Types**: Configurable maintenance types with periods
- **Inspection Types**: Configurable inspection types with frequencies

### User Interface
- Modern Bootstrap 5 responsive design
- Dashboard with equipment status overview
- Advanced filtering and sorting
- Intuitive navigation with dropdown menus
- Custom 404 error page
- Success/error message notifications

## 🛠️ Technologies Used

- **Backend**: Django 6.0.2 (Python 3.12)
- **Database**: PostgreSQL (development: SQLite)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Libraries**:
  - `python-dateutil` - for advanced date calculations
  - `psycopg2-binary` - PostgreSQL adapter
  - `python-dotenv` - environment variable management

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- **PostgreSQL 13+** (recommended for production)
  - For development, SQLite is also supported
- pip (Python package manager)

### Step 1: Clone the repository
```bash
git clone <your-repository-url>
cd equipmentsystem
```

### Step 2: Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Variables
Create a `.env` file in the project root:

#### Option 1: PostgreSQL (Recommended for Production)
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/equipmentdb

# PostgreSQL connection example:
# DATABASE_URL=postgresql://postgres:your_password@localhost:5432/lab_equipment
```

#### Option 2: SQLite (For Development/Testing)
```env
DEBUG=True
SECRET_KEY=your-secret-key-here

# Leave DATABASE_URL empty or comment it out to use SQLite
# DATABASE_URL=
```

**Note:** The application is configured to use **PostgreSQL by default** in production. For local development, you can use SQLite by not setting the DATABASE_URL environment variable. The settings.py will automatically fall back to SQLite.

### Step 5: Database Setup

#### For PostgreSQL:
```bash
# Create PostgreSQL database
createdb lab_equipment

# Or using psql:
psql -U postgres
CREATE DATABASE lab_equipment;
\q

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### For SQLite (development only):
```bash
# Run migrations (db.sqlite3 will be created automatically)
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Step 6: Run the development server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to access the application.

## 📁 Project Structure

```
equipmentsystem/
├── config/                 # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── equipment/             # Equipment management app
│   ├── models.py         # Equipment, Manufacturer, EquipmentCategory
│   ├── views.py          # CRUD views
│   ├── forms.py          # Forms with validation
│   ├── urls.py
│   └── templates/
│       └── equipment/    # Equipment templates
├── maintenance/          # Maintenance management app
│   ├── models.py        # MaintenanceType, MaintenanceRecord
│   ├── views.py         # CRUD views
│   ├── forms.py         # Forms with auto-date calculation
│   ├── urls.py
│   └── templates/
│       └── maintenance/ # Maintenance templates
├── inspections/         # Inspection management app
│   ├── models.py       # InspectionType, Inspection
│   ├── views.py        # CRUD views
│   ├── forms.py        # Forms with auto-date calculation
│   ├── urls.py
│   └── templates/
│       └── inspections/ # Inspection templates
├── manage.py
├── requirements.txt
└── README.md
```

## 🎯 Key Features Explained

### Automatic Status Calculation
Equipment status is automatically calculated based on:
- **Operational**: All maintenance and inspections are up-to-date
- **Calibration Required**: Maintenance is overdue (next_due_date < today)
- **Under Maintenance**: Inspection is overdue or needs attention
- **Out of Service**: Last inspection failed

The status updates automatically when maintenance or inspection records are saved.

### Automatic Date Calculation
- **Maintenance Records**: `next_due_date` is automatically calculated from `performed_date + maintenance_type.period_months`
- **Inspections**: `next_inspection_date` is automatically calculated from `inspection_date + inspection_type.frequency`

### Many-to-Many Relationships
Equipment can have multiple `required_maintenance_types` (e.g., a balance requires both annual calibration and quarterly technical service).

## 🔐 Admin Panel

Access the Django admin panel at http://127.0.0.1:8000/admin/

Default admin credentials (after `createsuperuser`):
- Username: (your chosen username)
- Password: (your chosen password)

## 📚 Database Models

### Core Models
1. **Equipment**: Laboratory equipment with auto-calculated status
2. **Manufacturer**: Equipment manufacturers
3. **EquipmentCategory**: Equipment categories
4. **MaintenanceType**: Types of maintenance activities
5. **MaintenanceRecord**: Maintenance history with auto dates
6. **InspectionType**: Types of inspections with frequencies
7. **Inspection**: Inspection history with auto dates

### Relationships
- Equipment → Manufacturer (ForeignKey)
- Equipment → EquipmentCategory (ForeignKey)
- Equipment ↔ MaintenanceType (ManyToMany)
- MaintenanceRecord → Equipment (ForeignKey)
- MaintenanceRecord → MaintenanceType (ForeignKey)
- Inspection → Equipment (ForeignKey)
- Inspection → InspectionType (ForeignKey)

## 🚀 Usage

### Adding Equipment
1. Navigate to **Equipment → Add Equipment**
2. Fill in the required fields:
   - ASSET Number (e.g., EQ-001)
   - Name, Model, Serial Number
   - Select Category and Manufacturer
   - Choose Required Maintenance Types
3. The status will be set to "Operational" by default

### Recording Maintenance
1. Navigate to **Maintenance → Add Maintenance**
2. Select Equipment and Maintenance Type
3. Enter Performed Date
4. **Next Due Date is calculated automatically**
5. Fill in results, certificate number, cost (optional)

### Recording Inspection
1. Navigate to **Inspections → Add Inspection**
2. Select Equipment and Inspection Type
3. Enter Inspection Date and Status
4. **Next Inspection Date is calculated automatically**
5. Document findings and corrective actions

### Managing Reference Data
Use the **Setup** menu to manage:
- Manufacturers
- Equipment Categories
- Maintenance Types (with periods in months)
- Inspection Types (with frequencies)

## 🐛 Troubleshooting

### Database Connection Errors
- Check `.env` file for correct DATABASE_URL
- Ensure PostgreSQL server is running
- Verify database credentials

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Migrations Issues
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📝 License

This project is developed for educational purposes as part of Django Basics Course @ SoftUni.

## 👥 Author

Developed by [Your Name] - Django Basics Regular Exam Project

## 📞 Support

For issues or questions, please contact [your-email@example.com]

---

**Note**: This application is designed for pharmaceutical and analytical laboratory equipment management in compliance with GMP, ISO, and EDQM guidelines.

