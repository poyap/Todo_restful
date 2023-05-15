from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView, 
    RetrieveAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from todo.models import Task, Project
from todo.api.serializers import TaskSerializer, ProjectSerializer
from .mixins import (
    IsProjectManagerPermissionMixin, 
    ValidUserPermissionMixin,
    UserQuerySetMixin, 
)


class ProjectTasksListAPIView(ValidUserPermissionMixin, UserQuerySetMixin, ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
class UserTasksListAPIView(ValidUserPermissionMixin, UserQuerySetMixin, ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()


class ProjectManagerTaskAssignAPIView(IsProjectManagerPermissionMixin, CreateAPIView):
    serializer_class = TaskSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class ProjectListCreateAPIView(IsProjectManagerPermissionMixin, ListCreateAPIView):
    """
    List all projects or create one.
    """
    serializer_class = ProjectSerializer
    
    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(manager=self.request.user)
