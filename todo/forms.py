from django import forms

from .models import Task, Project


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'start_at',
            'deadline',
            'status',
        ]

class TaskCreateForm(forms.ModelForm):
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