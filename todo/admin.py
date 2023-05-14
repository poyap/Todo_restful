from django.contrib import admin
from .models import Project, Task
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['manager']
    list_filter = ['manager']
admin.site.register(Project, ProjectAdmin, )
admin.site.register(Task)