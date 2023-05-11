from django.db import models

from accounts.models import CustomUser

STATUS_CHOICES = (
    (1, 'In Progress'),
    (2, 'Done'),
    (3, 'Not Started'),
    (4, 'Archived'),
)
class CommonFieldMixin(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    class Meta:
        abstract = True
        
    def get_status_name(self):
        return self.get_status_display()

class Project(CommonFieldMixin):
    manager = models.ForeignKey(CustomUser,
        on_delete=models.SET_NULL,
        null=True, related_name='projects',)
    
    class Meta:
        db_table = 'projects'
        ordering = ('-created_at',)
        
    def __str__(self):
        return self.name

class Task(CommonFieldMixin):
    developers = models.ManyToManyField(CustomUser)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    class Meta:
        db_table = 'tasks'
        ordering = ('-deadline',)

    def __str__(self):
        return self.name
        