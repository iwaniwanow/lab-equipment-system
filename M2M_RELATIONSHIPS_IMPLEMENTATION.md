# Many-to-Many Relationships Implementation

## Обобщение
Успешно имплементирани **Many-to-Many** relationships в Equipment System:

### 1. **Tag Model** (Тагове/Етикети)
- **Описание**: Етикети за категоризация на оборудването
- **M2M връзка**: `Equipment` ↔ `Tag` (many-to-many)
- **Полета**:
  - `name`: Име на таг (уникално)
  - `color`: Цвят в hex формат (#007bff по подразбиране)
  - `description`: Описание
  - `is_active`: Активен статус
  - `created_at`: Дата на създаване
  - `equipment`: ManyToManyField към Equipment

- **Методи**:
  - `equipment_count()`: Връща броя на свързаното оборудване
  - `__str__()`: Връща името на тага

### 2. **Document Model** (Документи)
- **Описание**: Документи свързани с оборудването
- **M2M връзка**: `Equipment` ↔ `Document` (many-to-many)
- **Полета**:
  - `name`: Име на документ
  - `document_type`: Тип документ (choices):
    - `manual` - Ръководство
    - `certificate` - Сертификат
    - `protocol` - Протокол
    - `validation` - Валидация
    - `sop` - SOP (Standard Operating Procedure)
    - `drawing` - Чертеж
    - `photo` - Снимка
    - `other` - Друг
  - `file`: FileField за качване на файл
  - `description`: Описание
  - `uploaded_by`: ForeignKey към User (кой е качил)
  - `uploaded_at`: Дата на качване
  - `version`: Версия на документа
  - `is_active`: Активен статус
  - `equipment`: ManyToManyField към Equipment

- **Методи**:
  - `equipment_count()`: Връща броя на свързаното оборудване
  - `__str__()`: Връща име и тип на документа

## Админ Панел

### TagAdmin
- **List Display**: name, color, equipment_count, is_active
- **Filters**: is_active
- **Search**: name, description
- **Special**: filter_horizontal за лесно управление на M2M връзката

### DocumentAdmin
- **List Display**: name, document_type, uploaded_by, uploaded_at, equipment_count, is_active
- **Filters**: document_type, is_active, uploaded_at
- **Search**: name, description
- **Special**: 
  - filter_horizontal за лесно управление на M2M връзката
  - Auto-set uploaded_by на текущия потребител при създаване
  - Readonly fields: uploaded_at, uploaded_by

## Миграции
- ✅ **Migration 0009**: Създадени Tag и Document модели с M2M relationships

## Използване

### Добавяне на тагове към оборудване:
```python
# Създаване на таг
tag = Tag.objects.create(
    name='Критично',
    color='#FF0000',
    description='Критично оборудване за производството'
)

# Добавяне на оборудване към таг
equipment = Equipment.objects.get(id=1)
tag.equipment.add(equipment)

# Или обратно
equipment.tags.add(tag)

# Извличане на всички тагове за оборудване
equipment.tags.all()

# Извличане на всичко оборудване с даден таг
Tag.objects.get(name='Критично').equipment.all()
```

### Работа с документи:
```python
# Създаване на документ
doc = Document.objects.create(
    name='Ръководство за употреба pH метър',
    document_type='manual',
    file='path/to/file.pdf',
    uploaded_by=request.user,
    version='1.0'
)

# Свързване с оборудване
doc.equipment.add(equipment1, equipment2)

# Извличане на всички документи за оборудване
equipment.documents.all()

# Филтриране по тип
equipment.documents.filter(document_type='manual')
```

## Предимства на M2M Relationships

1. **Гъвкавост**: Едно оборудване може да има много тагове и документи
2. **Повторна употреба**: Един документ може да се използва за много оборудване
3. **Лесно търсене**: Можете бързо да намерите всичко оборудване с даден таг
4. **Организация**: По-добра организация и категоризация на данните

## Следващи стъпки

Възможни разширения:
- [ ] API endpoints за работа с тагове и документи
- [ ] Frontend UI за управление на тагове и документи
- [ ] Bulk операции за добавяне на тагове към множество оборудване
- [ ] Версиониране на документи
- [ ] Права за достъп до документи
- [ ] Търсене и филтриране по тагове в Equipment ListView

## Фиксирани проблеми

1. ✅ **UserProfileForm**: Променено на `UserProfileUpdateForm` в users/views.py
2. ✅ **UserDetailView**: Премахнат неизползван URL pattern
3. ✅ **custom_404**: Добавен в equipment/views.py

## Статус
🟢 **READY FOR PRODUCTION**

Всички миграции са приложени и сървърът работи нормално.

