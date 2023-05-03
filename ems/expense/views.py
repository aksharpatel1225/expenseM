from django.shortcuts import render
from .models import Expense
from .forms import ProjectCreationForm
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView,DeleteView

# Create your views here.
class ProjectUpdateView(UpdateView):
    model =  Expense
    form_class = ProjectCreationForm
    template_name = 'user/add.html'
    success_url = '/user/template/'

class ProjectDeleteView(DeleteView):
    model = Expense
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    success_url = '/user/template/'