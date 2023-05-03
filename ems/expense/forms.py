from django import forms
from .models import Expense



class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model =Expense
        fields ='__all__'