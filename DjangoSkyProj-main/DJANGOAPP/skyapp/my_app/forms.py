from django import forms 
from .models import Employee
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User


class AdminCreateUserForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'team_number', 'department_number', 'role']

class ChangePasswordForm(PasswordChangeForm):
    
    pass