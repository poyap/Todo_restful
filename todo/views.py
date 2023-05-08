from django.shortcuts import render
from django.views.generic import (
    ListView, 
    CreateView,
    DetailView,
    UpdateView
    )


class TaskCreateView(CreateView):
    pass

class TaskRetrieveView(DetailView):
    pass


class ProjectCreateView(CreateView):
    pass