from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied

from todo.models import Task, Project, STATUS_CHOICES
from accounts.models import CustomUser


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(STATUS_CHOICES, source='get_status_name')
    class Meta:
        model = Project
        fields = [
            'id',
            'name', 
            'description', 
            'start_at', 
            'deadline',
            'status',
        ]
    # add the actual field name to the validated data
    def create(self, validated_data):
        status = validated_data.pop('get_status_name')
        validated_data['status'] = status
        validated_data['manager'] = self.context.get('request').user
        return super().create(validated_data)

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(STATUS_CHOICES, source='get_status_name')
   
    class Meta:
        model = Task
        fields = [
            'id',
            'name', 
            'description', 
            'developers',
            'project', 
            'start_at', 
            'deadline', 
            'status',
        ]
    
    # add the actual field name to the validated data
    def create(self, validated_data):
        validated_data['status'] = validated_data.pop('get_status_name')
        project = validated_data['project']
        if project.manager != self.context.get('request').user:
            raise PermissionDenied('You are not the creator of the project!!')

        return super().create(validated_data)
    
    # filter queryset to show only manager's projects
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('user')
        if user:
            self.fields['project'].queryset = user.projects.all()
        
