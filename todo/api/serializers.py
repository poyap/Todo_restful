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
    developers_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = [
            'id',
            'name', 
            'description', 
            'developers',
            'developers_detail', 
            'project', 
            'start_at', 
            'deadline', 
            'status',
        ]
    
    def get_developers_detail(self, obj):
        developers = obj.developers.all()
        return [{'username':dev.username,
            'user_tasks':reverse('todo:user-tasks',
            kwargs={'project_id':obj.project.id,
            'username':dev.username},),   
            } for dev in developers
        ]
        
    # add the actual field name to the validated data
    def create(self, validated_data):
        status = validated_data.pop('get_status_name')
        validated_data['status'] = status
        project = validated_data['project']
        if project.manager.id != self.context.get('request').user.id:
            raise PermissionDenied('You are not the creator of the project!!')
            return
        return super().create(validated_data)
    
    # filter queryset to show only manager's projects
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request:
            self.fields['project'].queryset = Project.objects.filter(manager=request.user)
