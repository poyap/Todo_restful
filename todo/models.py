from django.db import models

from accounts.models import User


class CommonFieldMixin(models.Model):
    status_choices = (
        (1, 'In Progress'),
        (2, 'Done'),
        (3, 'Not Started'),
        (4, 'Archived'),
    )
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices)

    class Meta:
        abstract = True

class Project(CommonFieldMixin):
    manager = models.ForeignKey(User, related_name='projects')
    
    class Meta:
        db_table = 'projects'
        ordering = ('-created')

    def __str__(self):
        return f'Project {self.name} created by {self.manager.username} at {self.created}'

class Task(CommonFieldMixin):
    developer = models.ForeignKey(User, related_name='tasks') 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        db_table = 'tasks'
        ordering = ('-deadline')

    def __str__(self):
        return f'Task {self.name} created by {self.developer.username} at {self.created}'
        
    
        