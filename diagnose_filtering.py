"""
Диагностичен скрипт за проверка на филтрирането на типове поддръжка
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from equipment.models import Technician, Department
from maintenance.models import MaintenanceType

print("=" * 60)
print("ДИАГНОСТИКА НА ФИЛТРИРАНЕ НА ТИПОВЕ ПОДДРЪЖКА")
print("=" * 60)

# Проверка на типове поддръжка
print("\n1. НАЛИЧНИ ТИПОВЕ ПОДДРЪЖКА:")
print("-" * 60)
for mt in MaintenanceType.objects.all():
    print(f"  - {mt.name} ({mt.type}) - {mt.get_type_display()}")

# Проверка на звена
print("\n2. НАЛИЧНИ ЗВЕНА:")
print("-" * 60)
for dept in Department.objects.all():
    print(f"  - {dept.code} - {dept.name}")

# Проверка на техници с потребители
print("\n3. ТЕХНИЦИ СЪС СВЪРЗАНИ ПОТРЕБИТЕЛИ:")
print("-" * 60)
for tech in Technician.objects.filter(user__isnull=False):
    user = tech.user
    role = user.profile.role if hasattr(user, 'profile') else 'N/A'
    dept = tech.department.code if tech.department else 'БЕЗ ЗВЕНО'
    print(f"  - {tech.get_full_name()}")
    print(f"    Потребител: {user.username} (роля: {role})")
    print(f"    Звено: {dept} - {tech.department.name if tech.department else 'N/A'}")

    # Симулация на филтриране
    if tech.department:
        dept_code = tech.department.code.upper()
        dept_full_name = tech.department.full_name if tech.department.full_name else ''

        allowed_types = []

        # Метрологичен отдел (МО) → Калибровки
        if dept_code == 'МО':
            allowed_types = ['calibration']
            print(f"    → ЩЕ ВИЖДА: Калибровки")

        # Технически отдел (ТО) → Ремонт и Технически преглед
        elif dept_code == 'ТО':
            allowed_types = ['repair', 'technical_service']
            print(f"    → ЩЕ ВИЖДА: Ремонт, Технически преглед")

        # Лаборатории и контрол (ККП, КИОМ, НР, ОК, КК, ФХК) → Валидиране
        elif dept_code in ['ККП', 'КИОМ', 'НР', 'ОК', 'КК', 'ФХК']:
            allowed_types = ['validation']
            print(f"    → ЩЕ ВИЖДА: Валидиране")

        else:
            print(f"    → ВНИМАНИЕ: Звено {dept_code} ({dept_full_name}) не е в списъка!")
            print(f"       Ще вижда ВСИЧКИ типове поддръжка")


        if allowed_types:
            filtered = MaintenanceType.objects.filter(type__in=allowed_types)
            print(f"    Филтрирани записи: {filtered.count()}")
            for mt in filtered:
                print(f"      * {mt.name}")
    print()

print("=" * 60)
print("КРАЙ НА ДИАГНОСТИКАТА")
print("=" * 60)

