from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматично създаване на UserProfile при създаване на нов потребител
    """
    if created:
        # Use get_or_create to avoid duplicates
        UserProfile.objects.get_or_create(
            user=instance,
            defaults={'role': 'viewer', 'is_approved': False}
        )


# Removed the save_user_profile signal as it causes issues
# Profile should be saved explicitly when needed



@receiver(post_save, sender=UserProfile)
def create_technician_profile(sender, instance, **kwargs):
    """
    Автоматично създаване на Technician профил, когато потребителят е одобрен
    и има роля 'technician'
    """
    from equipment.models import Technician

    # Проверка дали потребителят е одобрен и е техник
    if instance.is_approved and instance.role == 'technician':
        # Проверка дали вече има Technician профил
        if not hasattr(instance.user, 'technician_profile'):
            # Създаване на Technician профил
            Technician.objects.create(
                user=instance.user,
                first_name=instance.user.first_name,
                last_name=instance.user.last_name,
                email=instance.user.email,
                phone=instance.phone or '',
                department=instance.department,
                specialization='general',
                is_active=True
            )


