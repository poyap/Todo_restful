from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AssignTaskPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.role == 'manager':
            raise PermissionDenied('You are not allowed to create project.')
            return False
        return True
        