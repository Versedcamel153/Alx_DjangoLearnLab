from rest_framework.permissions import BasePermission
from rest_framework import permissions
class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit or delete an object.
    """

    def has_permission(self, request, view):
        # Allow read-only access to all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow access only to admin users for unsafe methods
        return request.user and request.user.is_staff