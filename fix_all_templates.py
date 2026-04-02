"""
Поправка на всички темплейти с грешни кавички и липсващи permission checks
"""
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
equipment_templates = os.path.join(base_dir, 'equipment', 'templates', 'equipment')

files_to_fix = {
    'category_detail.html': [
        ("{% if user.is_authenticated %}", "{% if user|can_modify_data %}"),
        ("{% url \\'equipment:category_update\\'", "{% url 'equipment:category_update'"),
    ],
    'technician_detail.html': [
        ("<a href=\"{% url 'equipment:technician_update' technician.pk %}\" class=\"btn btn-secondary\">", None),  # Само check
    ],
    'department_detail.html': [
        ("<a href=\"{% url 'equipment:department_update' dept.pk %}\" class=\"btn btn-secondary\">", None),
    ],
    'location_detail.html': [
        ("<a href=\"{% url 'equipment:location_update' location.pk %}\" class=\"btn btn-secondary\">", None),
    ],
}

print("Ръчна поправка на темплейтите...")
print("=" * 60)

# За всеки файл
for filename in ['category_detail.html', 'technician_detail.html', 'department_detail.html', 'location_detail.html']:
    filepath = os.path.join(equipment_templates, filename)

    if not os.path.exists(filepath):
        print(f"❌ Не съществува: {filename}")
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Общи замени
        content = content.replace("{% url \\'equipment:", "{% url 'equipment:")
        content = content.replace("\\' ", "' ")
        content = content.replace("\\'%}", "'%}")

        # Добавяне на permission check ако няма
        if "{% if user|can_modify_data %}" not in content and '<a href="{% url \'equipment:' in content and '_update' in content:
            # Намираме секцията с бутони за редактиране
            lines = content.split('\n')
            new_lines = []
            in_buttons = False

            for i, line in enumerate(lines):
                if '_update' in line and '<a href="{% url' in line and not in_buttons:
                    # Започваме секция с бутони
                    new_lines.append("    {% if user|can_modify_data %}")
                    new_lines.append("    <div>")
                    in_buttons = True
                    new_lines.append(line)
                elif in_buttons and ('</div>' in line or (i + 1 < len(lines) and '</div>' not in lines[i+1] and '<a' not in lines[i+1])):
                    new_lines.append(line)
                    if '</div>' in line:
                        new_lines.append("    {% endif %}")
                        in_buttons = False
                else:
                    new_lines.append(line)

            content = '\n'.join(new_lines)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Поправен: {filename}")
        else:
            print(f"ℹ️ Без промени: {filename}")

    except Exception as e:
        print(f"❌ Грешка при {filename}: {e}")

print("=" * 60)
print("✅ Готово!")

