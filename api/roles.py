from rest_framework import permissions


class IsPayingUser(permissions.BasePermission):
    """Permissions for Paying custumers"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='PayingUser').exists()


class IsFreeUser(permissions.BasePermission):
    """Permissions for Free Users"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='FreeUser').exists()
