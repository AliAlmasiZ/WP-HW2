from rest_framework.permissions import BasePermission
from .models import User

class IsServiceProvider(BasePermission):
    """
    Custom permission to only allow users with the 'provider' role.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'provider')
    

class isSupportOrAdmin(BasePermission):
    """
    Custom permission to only allow users with the 'support' or 'admin' roles.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['support', 'admin'])
    

