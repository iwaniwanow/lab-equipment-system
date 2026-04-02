"""
Script to fix URL namespace references in all HTML templates.
"""
import os
import re

# Define URL replacements: (pattern, replacement)
URL_FIXES = [
    # Equipment URLs
    (r"{% url 'dashboard'", "{% url 'equipment:dashboard'"),
    (r"{% url 'equipment_list'", "{% url 'equipment:equipment_list'"),
    (r"{% url 'equipment_detail'", "{% url 'equipment:equipment_detail'"),
    (r"{% url 'equipment_create'", "{% url 'equipment:equipment_create'"),
    (r"{% url 'equipment_update'", "{% url 'equipment:equipment_update'"),
    (r"{% url 'equipment_delete'", "{% url 'equipment:equipment_delete'"),

    # Manufacturer URLs
    (r"{% url 'manufacturer_list'", "{% url 'equipment:manufacturer_list'"),
    (r"{% url 'manufacturer_detail'", "{% url 'equipment:manufacturer_detail'"),
    (r"{% url 'manufacturer_create'", "{% url 'equipment:manufacturer_create'"),
    (r"{% url 'manufacturer_update'", "{% url 'equipment:manufacturer_update'"),
    (r"{% url 'manufacturer_delete'", "{% url 'equipment:manufacturer_delete'"),

    # Category URLs
    (r"{% url 'category_list'", "{% url 'equipment:category_list'"),
    (r"{% url 'category_detail'", "{% url 'equipment:category_detail'"),
    (r"{% url 'category_create'", "{% url 'equipment:category_create'"),
    (r"{% url 'category_update'", "{% url 'equipment:category_update'"),
    (r"{% url 'category_delete'", "{% url 'equipment:category_delete'"),

    # Department URLs
    (r"{% url 'department_list'", "{% url 'equipment:department_list'"),
    (r"{% url 'department_detail'", "{% url 'equipment:department_detail'"),
    (r"{% url 'department_create'", "{% url 'equipment:department_create'"),
    (r"{% url 'department_update'", "{% url 'equipment:department_update'"),
    (r"{% url 'department_delete'", "{% url 'equipment:department_delete'"),

    # Location URLs
    (r"{% url 'location_list'", "{% url 'equipment:location_list'"),
    (r"{% url 'location_detail'", "{% url 'equipment:location_detail'"),
    (r"{% url 'location_create'", "{% url 'equipment:location_create'"),
    (r"{% url 'location_update'", "{% url 'equipment:location_update'"),
    (r"{% url 'location_delete'", "{% url 'equipment:location_delete'"),

    # Technician URLs
    (r"{% url 'technician_list'", "{% url 'equipment:technician_list'"),
    (r"{% url 'technician_detail'", "{% url 'equipment:technician_detail'"),
    (r"{% url 'technician_create'", "{% url 'equipment:technician_create'"),
    (r"{% url 'technician_update'", "{% url 'equipment:technician_update'"),
    (r"{% url 'technician_delete'", "{% url 'equipment:technician_delete'"),

    # Maintenance URLs
    (r"{% url 'maintenance_list'", "{% url 'maintenance:maintenance_list'"),
    (r"{% url 'maintenance_detail'", "{% url 'maintenance:maintenance_detail'"),
    (r"{% url 'maintenance_create'", "{% url 'maintenance:maintenance_create'"),
    (r"{% url 'maintenance_update'", "{% url 'maintenance:maintenance_update'"),
    (r"{% url 'maintenance_delete'", "{% url 'maintenance:maintenance_delete'"),
    (r"{% url 'maintenance_type_list'", "{% url 'maintenance:maintenance_type_list'"),
    (r"{% url 'maintenance_type_detail'", "{% url 'maintenance:maintenance_type_detail'"),
    (r"{% url 'maintenance_type_create'", "{% url 'maintenance:maintenance_type_create'"),
    (r"{% url 'maintenance_type_update'", "{% url 'maintenance:maintenance_type_update'"),
    (r"{% url 'maintenance_type_delete'", "{% url 'maintenance:maintenance_type_delete'"),

    # Inspection URLs
    (r"{% url 'inspection_list'", "{% url 'inspections:inspection_list'"),
    (r"{% url 'inspection_detail'", "{% url 'inspections:inspection_detail'"),
    (r"{% url 'inspection_create'", "{% url 'inspections:inspection_create'"),
    (r"{% url 'inspection_update'", "{% url 'inspections:inspection_update'"),
    (r"{% url 'inspection_delete'", "{% url 'inspections:inspection_delete'"),
    (r"{% url 'inspection_type_list'", "{% url 'inspections:inspection_type_list'"),
    (r"{% url 'inspection_type_detail'", "{% url 'inspections:inspection_type_detail'"),
    (r"{% url 'inspection_type_create'", "{% url 'inspections:inspection_type_create'"),
    (r"{% url 'inspection_type_update'", "{% url 'inspections:inspection_type_update'"),
    (r"{% url 'inspection_type_delete'", "{% url 'inspections:inspection_type_delete'"),
]

def fix_template(filepath):
    """Fix URL namespace references in a single template file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = []

        for pattern, replacement in URL_FIXES:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made.append(pattern)

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made

        return False, []
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False, []

def main():
    """Main function to process all templates."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dirs = ['equipment', 'inspections', 'maintenance']

    total_files = 0
    fixed_files = 0

    for templates_dir in templates_dirs:
        templates_path = os.path.join(base_dir, templates_dir, 'templates')
        if not os.path.exists(templates_path):
            continue

        for root, dirs, files in os.walk(templates_path):
            for file in files:
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    total_files += 1

                    fixed, changes = fix_template(filepath)
                    if fixed:
                        fixed_files += 1
                        print(f"✓ Fixed: {filepath}")
                        print(f"  Changes: {len(changes)} URL(s) updated")

    print(f"\n{'='*60}")
    print(f"Summary: Fixed {fixed_files} out of {total_files} template files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

