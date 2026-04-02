"""
Скрипт за автоматично добавяне на {% load permission_tags %} и замяна на проверки
в темплейтите
"""
import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
equipment_templates = os.path.join(base_dir, 'equipment', 'templates', 'equipment')

# Списък с темплейти които трябва да се актуализират
templates_to_fix = [
    'manufacturer_list.html',
    'category_list.html',
    'technician_list.html',
    'department_list.html',
    'location_list.html',
    'manufacturer_detail.html',
    'category_detail.html',
    'technician_detail.html',
    'department_detail.html',
    'location_detail.html',
]

for template_name in templates_to_fix:
    filepath = os.path.join(equipment_templates, template_name)

    if not os.path.exists(filepath):
        print(f"❌ Файлът не съществува: {template_name}")
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Проверка дали вече има {% load permission_tags %}
        if '{% load permission_tags %}' not in content:
            # Добавяме след {% extends %}
            content = re.sub(
                r'({% extends [\'"]equipment/base\.html[\'"] %})',
                r'\1\n{% load permission_tags %}',
                content
            )

        # Замяна на {% if user.is_authenticated %} с {% if user|can_modify_data %}
        # за бутони за създаване/редактиране/изтриване

        # Бутон "Добави" / "Създай" / "Нов"
        content = re.sub(
            r'{% if user\.is_authenticated %}\s*<div class="col-auto">\s*<a href="{% url [\'"]equipment:(\w+)_create[\'"]',
            r'{% if user|can_modify_data %}\n    <div class="col-auto">\n        <a href="{% url \'equipment:\1_create\'',
            content
        )

        # Бутони за редактиране и изтриване в детайли
        content = re.sub(
            r'{% if user\.is_authenticated %}\s*<div(?:[^>]*)>\s*<a href="{% url [\'"]equipment:(\w+)_update[\'"]',
            r'{% if user|can_modify_data %}\n    <div class="col-auto">\n        <a href="{% url \'equipment:\1_update\'',
            content
        )

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Актуализиран: {template_name}")
        else:
            print(f"ℹ️ Без промени: {template_name}")

    except Exception as e:
        print(f"❌ Грешка при обработка на {template_name}: {e}")

print("\n✅ Готово!")

