from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView, 
    RetrieveAPIView,
)
from todo.models import Task, Project
from todo.api.serializers import TaskSerializer, ProjectSerializer
from .permissions import AssignTaskPermission


class ProjectTasksListAPIView(RetrieveAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related('tasks').all()

class ProjectUserTasksListAPIView(RetrieveAPIView):
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Task.objects.prefetch_related('project').filter(developer__username=request.username)
        return super().get(request, *args, **kwargs)

class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [AssignTaskPermission, ]


