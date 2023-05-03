from django import forms
from django.contrib.auth import (password_validation,)
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        help_text=password_validation.password_validators_help_text_html(),
        label="Password",
        widget=forms.PasswordInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Password'}), )
    password2 = forms.CharField(
        help_text="Enter the same password as before, for verification.",
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Confirm Password'}), )

    class Meta:
        model = User
        fields = ("email", "fullname", "password1", "password2")
        widgets = {
            'fullname': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'E-Mail'})
        }