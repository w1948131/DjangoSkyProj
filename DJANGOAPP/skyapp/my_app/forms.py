from django import forms 
from .models import Employee


class AdminCreateUserForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'team_number', 'department_number', 'role']