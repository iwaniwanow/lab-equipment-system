import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

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
print(f"   ✓ Tag: {tag_critical}")

tag_gmp, _ = Tag.objects.get_or_create(
    name='GMP',
    defaults={'color': '#0066CC', 'description': 'GMP валидирано оборудване'}
)
print(f"   ✓ Tag: {tag_gmp}")

tag_new, _ = Tag.objects.get_or_create(
    name='Ново',
    defaults={'color': '#00CC00', 'description': 'Ново оборудване'}
)
print(f"   ✓ Tag: {tag_new}")

# 2. Get some equipment
print("\n2. Getting Equipment...")
equipment_list = Equipment.objects.all()[:3]
print(f"   ✓ Found {equipment_list.count()} equipment items")

# 3. Add tags to equipment
print("\n3. Adding Tags to Equipment...")
if equipment_list.exists():
    eq1 = equipment_list.first()
    eq1.tags.add(tag_critical, tag_gmp)
    print(f"   ✓ Added 'Критично' and 'GMP' tags to {eq1}")
    print(f"   ✓ Equipment tags: {', '.join([t.name for t in eq1.tags.all()])}")

# 4. Query equipment by tag
print("\n4. Querying Equipment by Tag...")
critical_equipment = tag_critical.equipment.all()
print(f"   ✓ Tag: {tag_critical}")
print(f"   ✓ Equipment count: {tag_critical.equipment_count()}")
for eq in critical_equipment:
    print(f"     - {eq}")

# 5. Create a test document
print("\n5. Testing Documents...")
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
    print(f"   ✓ Document: {doc}")

    # Add equipment to document
    if equipment_list.exists():
        doc.equipment.add(equipment_list.first())
        print(f"   ✓ Added equipment to document")
        print(f"   ✓ Equipment count: {doc.equipment_count()}")

# 6. Statistics
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
for doc in Document.objects.all()[:5]:
    print(f"  {doc.name}: {doc.equipment_count()} equipment")

print("\n" + "=" * 60)
print("✓ M2M Relationships Test Complete!")
print("=" * 60)

