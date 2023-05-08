from rest_framework import serializers

from .models import Task, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name', 
            'description', 
            'manager',
            'start_at', 
            'deadline',
            'status',
        ]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name', 
            'description', 
            'developer', 
            'project', 
            'start_at', 
            'deadline', 
            'status',
        ]

