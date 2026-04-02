"""
Скрипт за поправка на грешни escape-нати кавички в темплейтите
"""
import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
equipment_templates = os.path.join(base_dir, 'equipment', 'templates', 'equipment')

# Намери всички HTML файлове
for root, dirs, files in os.walk(equipment_templates):
    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # Поправка на escape-нати кавички в url тагове
                # {% url \'equipment:something\' %} → {% url 'equipment:something' %}
                content = re.sub(r"{% url \\'([^']+)\\' %}", r"{% url '\1' %}", content)

                # Поправка на double escaped
                content = re.sub(r"{% url \\\\'([^']+)\\\\' %}", r"{% url '\1' %}", content)

                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Поправен: {filename}")

            except Exception as e:
                print(f"❌ Грешка при {filename}: {e}")

print("\n✅ Всички файлове са проверени и поправени!")

