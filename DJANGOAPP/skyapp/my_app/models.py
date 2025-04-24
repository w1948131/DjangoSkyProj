from django.db import models

# Create your models here.



class Employee(models.Model):
   ROLE_CHOICES = [
       ('engineer', 'Engineer'),
       ('teamleader', 'Team Leader'),
       ('departmentleader', 'Department Leader'),
       ('seniormanager', 'Senior Manager'),
       ('admin', 'Admin'),
   ]


   email = models.EmailField(unique=True)
   name = models.CharField(max_length=100)
   team_number = models.CharField(max_length=50)
   department_number = models.CharField(max_length=50)
   role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineer')
   registered = models.BooleanField(default=False)


   def __str__(self):
       return self.name
