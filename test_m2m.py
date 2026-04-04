"""
Test script for Many-to-Many Relationships
Run with: python manage.py shell < test_m2m.py
"""

from equipment.models import Equipment, Tag, Document
from django.contrib.auth.models import User

print("=" * 60)
print("Testing Many-to-Many Relationships")
print("=" * 60)

# 1. Create some tags
print("\n1. Creating Tags...")
tag_critical, _ = Tag.objects.get_or_create(
    name='Критично',
    defaults={'color': '#FF0000', 'description': 'Критично оборудване'}
)
print(f"   ✓ Created: {tag_critical}")

tag_gmp, _ = Tag.objects.get_or_create(
    name='GMP',
    defaults={'color': '#0066CC', 'description': 'GMP валидирано оборудване'}
)
print(f"   ✓ Created: {tag_gmp}")

tag_new, _ = Tag.objects.get_or_create(
    name='Ново',
    defaults={'color': '#00CC00', 'description': 'Ново оборудване'}
)
print(f"   ✓ Created: {tag_new}")

# 2. Get some equipment
print("\n2. Getting Equipment...")
equipment_list = Equipment.objects.all()[:3]
if equipment_list.exists():
    for eq in equipment_list:
        print(f"   ✓ Found: {eq}")
else:
    print("   ✗ No equipment found. Please create some equipment first.")

# 3. Add tags to equipment
print("\n3. Adding Tags to Equipment...")
if equipment_list.exists():
    eq1 = equipment_list.first()
    eq1.tags.add(tag_critical, tag_gmp)
    print(f"   ✓ Added 'Критично' and 'GMP' tags to {eq1}")

    if equipment_list.count() > 1:
        eq2 = equipment_list[1]
        eq2.tags.add(tag_new)
        print(f"   ✓ Added 'Ново' tag to {eq2}")

# 4. Query tags for equipment
print("\n4. Querying Tags for Equipment...")
if equipment_list.exists():
    eq1 = equipment_list.first()
    tags = eq1.tags.all()
    print(f"   Equipment: {eq1}")
    print(f"   Tags: {', '.join([t.name for t in tags])}")

# 5. Query equipment by tag
print("\n5. Querying Equipment by Tag...")
critical_equipment = tag_critical.equipment.all()
print(f"   Tag: {tag_critical}")
print(f"   Equipment count: {tag_critical.equipment_count()}")
if critical_equipment:
    for eq in critical_equipment:
        print(f"   - {eq}")

# 6. Create a test document (if we have a user)
print("\n6. Testing Documents...")
user = User.objects.first()
if user:
    doc, created = Document.objects.get_or_create(
        name='Тестов документ',
        defaults={
            'document_type': 'manual',
            'description': 'Тестово ръководство',
            'uploaded_by': user
        }
    )
    if created:
        print(f"   ✓ Created: {doc}")
    else:
        print(f"   ✓ Found existing: {doc}")

    # Add equipment to document
    if equipment_list.exists():
        doc.equipment.add(equipment_list.first())
        print(f"   ✓ Added equipment to document")
        print(f"   Equipment count: {doc.equipment_count()}")
else:
    print("   ✗ No users found. Cannot create test document.")

# 7. Statistics
print("\n" + "=" * 60)
print("Statistics:")
print("=" * 60)
print(f"Total Tags: {Tag.objects.count()}")
print(f"Total Documents: {Document.objects.count()}")
print(f"Total Equipment: {Equipment.objects.count()}")

print("\nTags breakdown:")
for tag in Tag.objects.all():
    print(f"  {tag.name} ({tag.color}): {tag.equipment_count()} equipment")

print("\nDocuments breakdown:")
for doc in Document.objects.all()[:5]:  # First 5
    print(f"  {doc.name}: {doc.equipment_count()} equipment")

print("\n" + "=" * 60)
print("✓ M2M Relationships Test Complete!")
print("=" * 60)

