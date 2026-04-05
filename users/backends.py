"""
Custom authentication backends for user approval system
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class ApprovedUserBackend(ModelBackend):
    """
    Authentication backend that only allows login for approved users
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user and check if they are approved
        Superusers can always login regardless of approval status
        """
        # First, use the default authentication
        user = super().authenticate(request, username=username, password=password, **kwargs)

        if user is None:
            return None

        # Superusers can always login
        if user.is_superuser:
            return user

        # Check if user has a profile and is approved
        if hasattr(user, 'profile'):
            if not user.profile.is_approved:
                # User is not approved, deny login
                return None
        else:
            # User has no profile (shouldn't happen), deny login
            return None

        return user

    def user_can_authenticate(self, user):
        """
        Override to check if user is approved in addition to being active
        """
        is_active = super().user_can_authenticate(user)

        if not is_active:
            return False

        if hasattr(user, 'profile'):
            return user.profile.is_approved

        return user.is_superuser

