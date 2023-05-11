from django.urls import path

from .api.views import (
    ProjectTasksListAPIView,
    UserTasksListAPIView,
    ProjectManagerTaskAssignAPIView,
    ProjectListCreateAPIView, 
)

app_name = 'todo'

urlpatterns = [
    path('api/project/<int:project_id>/tasks/', ProjectTasksListAPIView.as_view(), name='project-tasks'),
    path('api/project/<int:project_id>/user/<str:username>/tasks/', UserTasksListAPIView.as_view(), name='user-tasks'),
    path('api/task/assign/', ProjectManagerTaskAssignAPIView.as_view(), name='task-assign'),
    path('api/projects/', ProjectListCreateAPIView.as_view(), name='task-assign'),

]
