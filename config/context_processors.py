from users.models import UserProfile
from equipment.models import Technician
from django.contrib.auth.models import User


def admin_stats(request):
    """
    Context processor за статистики в админ панела
    """
    if not request.path.startswith('/admin/'):
        return {}

    return {
        'pending_users': UserProfile.objects.filter(is_approved=False).count(),
        'approved_users': UserProfile.objects.filter(is_approved=True).count(),
        'total_users': User.objects.count(),
        'total_technicians': Technician.objects.filter(is_active=True).count(),
    }

