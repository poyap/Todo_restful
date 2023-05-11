from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from todo.models import Project, Task
from accounts.models import CustomUser

class ProjectManagerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 1 or request.user.is_superuser:
            return True
        
        raise PermissionDenied('You are not allowed to Perform this action. Only Project managers are able to do so.')
        return False


class ValidUserPermission(permissions.BasePermission):
    """
    Ensures that developers within the project can see other users' task in the project or the project tasks.
    However, managers can see all.
    :Return: bool 
    """
    def has_permission(self, request, view):
        if request.user.role == 1 or request.user.is_superuser:
            return True
        elif request.user.role == 2:
            if Task.objects.filter(developers__in=[request.user]).exists():
                return True
            raise PermissionDenied('You are not allowed to Perform this action. Only users within a project can see the tasks list of that project.')
            return False
        