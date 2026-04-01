from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from equipment.models import Equipment
from maintenance.models import MaintenanceRecord
from inspections.models import Inspection


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Define groups and their permissions
        groups_permissions = {
            'Administrators': {
                'description': 'Full system access',
                'permissions': 'all'
            },
            'Managers': {
                'description': 'Can manage equipment, view all records, assign tasks',
                'permissions': [
                    # Equipment permissions
                    ('equipment', 'equipment', ['add', 'change', 'view']),
                    ('equipment', 'manufacturer', ['add', 'change', 'view']),
                    ('equipment', 'equipmentcategory', ['add', 'change', 'view']),
                    ('equipment', 'department', ['view']),
                    ('equipment', 'location', ['view']),
                    # Maintenance permissions
                    ('maintenance', 'maintenancerecord', ['add', 'change', 'view']),
                    ('maintenance', 'maintenancetype', ['view']),
                    # Inspection permissions
                    ('inspections', 'inspection', ['add', 'change', 'view']),
                ]
            },
            'Technicians': {
                'description': 'Can perform maintenance and inspections',
                'permissions': [
                    # Equipment permissions (view only)
                    ('equipment', 'equipment', ['view']),
                    ('equipment', 'manufacturer', ['view']),
                    ('equipment', 'equipmentcategory', ['view']),
                    # Maintenance permissions
                    ('maintenance', 'maintenancerecord', ['add', 'change', 'view']),
                    ('maintenance', 'maintenancetype', ['view']),
                    # Inspection permissions
                    ('inspections', 'inspection', ['add', 'change', 'view']),
                ]
            },
            'Operators': {
                'description': 'Can view equipment and create inspection records',
                'permissions': [
                    # Equipment permissions (view only)
                    ('equipment', 'equipment', ['view']),
                    # Inspection permissions
                    ('inspections', 'inspection', ['add', 'view']),
                ]
            },
            'Viewers': {
                'description': 'Read-only access to all records',
                'permissions': [
                    # Equipment permissions (view only)
                    ('equipment', 'equipment', ['view']),
                    ('equipment', 'manufacturer', ['view']),
                    ('equipment', 'equipmentcategory', ['view']),
                    # Maintenance permissions (view only)
                    ('maintenance', 'maintenancerecord', ['view']),
                    ('maintenance', 'maintenancetype', ['view']),
                    # Inspection permissions (view only)
                    ('inspections', 'inspection', ['view']),
                ]
            },
        }

        for group_name, config in groups_permissions.items():
            # Create or get group
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group already exists: {group_name}')
                )
                # Clear existing permissions
                group.permissions.clear()

            # Assign permissions
            if config['permissions'] == 'all':
                # Administrators get all permissions
                all_permissions = Permission.objects.all()
                group.permissions.set(all_permissions)
                self.stdout.write(
                    self.style.SUCCESS(f'  Assigned ALL permissions to {group_name}')
                )
            else:
                # Assign specific permissions
                for app_label, model_name, actions in config['permissions']:
                    try:
                        # Get content type for the model
                        content_type = ContentType.objects.get(
                            app_label=app_label,
                            model=model_name.lower()
                        )
                        
                        for action in actions:
                            # Get permission
                            codename = f'{action}_{model_name.lower()}'
                            try:
                                permission = Permission.objects.get(
                                    codename=codename,
                                    content_type=content_type
                                )
                                group.permissions.add(permission)
                                self.stdout.write(
                                    f'  Added permission: {codename} to {group_name}'
                                )
                            except Permission.DoesNotExist:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'  Permission not found: {codename}'
                                    )
                                )
                    except ContentType.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(
                                f'  Content type not found: {app_label}.{model_name}'
                            )
                        )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Successfully created all groups and permissions!')
        )
        self.stdout.write(
            self.style.SUCCESS('\nGroups created:')
        )
        for group_name, config in groups_permissions.items():
            self.stdout.write(f"  - {group_name}: {config['description']}")

