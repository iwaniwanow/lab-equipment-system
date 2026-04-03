from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Allow authenticated users full access (GET, POST, PUT, DELETE)
    - Anonymous users get NO access (not even read)
    """
    def has_permission(self, request, view):
        # Only authenticated users can access API
        return request.user and request.user.is_authenticated


class IsAdminOrManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Admin and Manager can do anything
    - Others can only read
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write operations, check role
        try:
            profile = request.user.profile
            return profile.role in ['admin', 'manager']
        except:
            return request.user.is_staff or request.user.is_superuser


class IsAdminOrManager(permissions.BasePermission):
    """
    Only Admin or Manager can access
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            profile = request.user.profile
            return profile.role in ['admin', 'manager']
        except:
            return request.user.is_staff or request.user.is_superuser

