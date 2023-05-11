from rest_framework import permissions

from .permissions import (
    ProjectManagerPermission,
    ValidUserPermission, 

)


class IsProjectManagerPermissionMixin:
    permission_classes = [permissions.IsAuthenticated, ProjectManagerPermission]

class ValidUserPermissionMixin:
    permission_classes = [permissions.IsAuthenticated, ValidUserPermission]

class UserQuerySetMixin:
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        username_url_kwargs = self.kwargs.get('username')
        # if request was for user's task base on username
        if username_url_kwargs:
            return qs.filter(project=self.kwargs['project_id'], developers__username__in=[username_url_kwargs])
        return qs.filter(project=self.kwargs['project_id'])
