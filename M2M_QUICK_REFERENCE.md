# Quick Reference - Many-to-Many Relationships

## 🏷️ Tags (Тагове)

### Create Tag
```python
from equipment.models import Tag

tag = Tag.objects.create(
    name='Критично',
    color='#FF0000',
    description='Критично оборудване за производството'
)
```

### Add Tag to Equipment
```python
equipment.tags.add(tag)
# or
tag.equipment.add(equipment)
```

### Remove Tag from Equipment
```python
equipment.tags.remove(tag)
```

### Get all Tags for Equipment
```python
tags = equipment.tags.all()
for tag in tags:
    print(f"{tag.name} ({tag.color})")
```

### Get all Equipment with specific Tag
```python
critical_equipment = Tag.objects.get(name='Критично').equipment.all()
```

### Filter Equipment by Tag
```python
from django.db.models import Q

# Equipment with 'Критично' OR 'GMP' tag
equipment = Equipment.objects.filter(
    Q(tags__name='Критично') | Q(tags__name='GMP')
).distinct()
```

---

## 📄 Documents (Документи)

### Create Document
```python
from equipment.models import Document

doc = Document.objects.create(
    name='Ръководство за употреба pH метър',
    document_type='manual',
    file='path/to/manual.pdf',
    description='Инструкции за работа с pH метър',
    uploaded_by=request.user,
    version='1.0'
)
```

### Add Equipment to Document
```python
doc.equipment.add(equipment1, equipment2, equipment3)
# or
equipment.documents.add(doc)
```

### Get all Documents for Equipment
```python
docs = equipment.documents.all()
for doc in docs:
    print(f"{doc.name} ({doc.get_document_type_display()})")
```

### Filter Documents by Type
```python
manuals = equipment.documents.filter(document_type='manual')
certificates = equipment.documents.filter(document_type='certificate')
```

### Get all Equipment with specific Document
```python
equipment_list = Document.objects.get(id=1).equipment.all()
```

---

## 🔍 Advanced Queries

### Equipment with multiple tags
```python
# Equipment that has BOTH 'Критично' AND 'GMP' tags
equipment = Equipment.objects.filter(
    tags__name='Критично'
).filter(
    tags__name='GMP'
)
```

### Equipment without tags
```python
equipment = Equipment.objects.filter(tags__isnull=True)
# or
equipment = Equipment.objects.annotate(
    tag_count=Count('tags')
).filter(tag_count=0)
```

### Equipment without documents
```python
equipment = Equipment.objects.filter(documents__isnull=True)
```

### Count tags per equipment
```python
from django.db.models import Count

equipment_with_counts = Equipment.objects.annotate(
    tag_count=Count('tags'),
    doc_count=Count('documents')
)

for eq in equipment_with_counts:
    print(f"{eq.name}: {eq.tag_count} tags, {eq.doc_count} documents")
```

### Get most used tags
```python
from django.db.models import Count

popular_tags = Tag.objects.annotate(
    usage_count=Count('equipment')
).order_by('-usage_count')[:10]
```

---

## 🎨 Color Codes for Tags

Предложени цветове:
```python
COLORS = {
    'Критично': '#FF0000',      # Red
    'GMP': '#0066CC',            # Blue
    'Ново': '#00CC00',           # Green
    'Legacy': '#999999',         # Gray
    'Под наблюдение': '#FF9900', # Orange
    'В ремонт': '#FFCC00',       # Yellow
    'Archived': '#666666',       # Dark Gray
}
```

---

## 📦 Bulk Operations

### Add same tag to multiple equipment
```python
tag = Tag.objects.get(name='GMP')
equipment_list = Equipment.objects.filter(category__name='pH метри')
tag.equipment.add(*equipment_list)
```

### Add multiple tags to one equipment
```python
tags = Tag.objects.filter(name__in=['Критично', 'GMP', 'Ново'])
equipment.tags.add(*tags)
```

### Clear all tags from equipment
```python
equipment.tags.clear()
```

### Clear all equipment from tag
```python
tag.equipment.clear()
```

---

## 🔐 Document Security (Future)

```python
# Check if user can view document
def can_view_document(user, document):
    if user.is_superuser:
        return True
    if user == document.uploaded_by:
        return True
    if hasattr(user, 'profile') and user.profile.role in ['admin', 'manager']:
        return True
    return False
```

---

## 📊 Statistics

```python
# Tag statistics
print(f"Total tags: {Tag.objects.count()}")
print(f"Active tags: {Tag.objects.filter(is_active=True).count()}")

# Document statistics
print(f"Total documents: {Document.objects.count()}")
print(f"Documents by type:")
for doc_type, label in Document.DOCUMENT_TYPE_CHOICES:
    count = Document.objects.filter(document_type=doc_type).count()
    print(f"  {label}: {count}")

# Equipment statistics
print(f"Equipment with tags: {Equipment.objects.filter(tags__isnull=False).distinct().count()}")
print(f"Equipment with documents: {Equipment.objects.filter(documents__isnull=False).distinct().count()}")
```

---

## 🌐 Admin Panel

**URL:** http://127.0.0.1:8000/admin/

### Quick Actions:
1. Navigate to **Equipment** → **Tags**
2. Click **Add Tag** to create new tag
3. Use **filter_horizontal** widget to add equipment
4. Navigate to **Equipment** → **Documents**
5. Upload file and select equipment

---

## 🧪 Testing

Run test script:
```bash
cd C:\Users\dbsupport2\PycharmProjects\equipmentsystem
python test_m2m_simple.py
```

Interactive shell:
```bash
python manage.py shell
>>> from equipment.models import Tag, Document, Equipment
>>> # Your code here
```

Alternative (via Django shell):
```bash
Get-Content test_m2m.py | python manage.py shell
```

---

**Last Updated:** 2026-04-03  
**Quick Reference Version:** 1.0

