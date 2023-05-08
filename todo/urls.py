from django.urls import path

from todo.api.views import (
    TaskCreateAPIView, 
    TaskListAPIView,
)
from .api.views import (
    TaskCreateAPIView, 
    ProjectTasksListAPIView, 
    ProjectUserTasksListAPIView,
)

urlpatterns = [
    path('api/task/create/', TaskCreateAPIView.as_view(), name='create_task'),
    path('api/<int:project_id>/tasks/', ProjectTasksListAPIView.as_view(), name='tasks_list'),
    path('api/<int:project_id>/<str:username>/tasks/', ProjectTasksListAPIView.as_view(), name='tasks_list'),
]
