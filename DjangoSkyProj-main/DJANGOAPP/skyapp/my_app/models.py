from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Class for Healthcard
class HealthCard(models.Model):
    # The health card is a foreign key for the user, so the user inherits the healthcard and its attributes.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health Card {self.user.username} - {self.created_at.date()}"

# Function to associate numerical value to the color choices from the vote.
class Vote(models.Model):
    COLOR_CHOICES = [
        (1, 'Red'),
        (2, 'Amber'),
        (3, 'Green'),
    ]

    #The votes are a foreign key for health card so health card will take all the attributes from the votes.
    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE, related_name='votes')

    #votes belong to a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    #votes have a category that they are attributed to
    category = models.CharField(max_length=100)

    #a color rating
    color = models.IntegerField(choices=COLOR_CHOICES)

    #as well as feedback
    feedback = models.TextField(blank=True, null=True)

    #date of when the vote was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['health_card', 'category']

    def get_color_display_name(self):
        return dict(self.COLOR_CHOICES)[self.color]
    
#Department class to hold the department name and the teams that belong to it
class Department(models.Model):

    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    def team_count(self):
        return self.teams.count()
    

    def can_add_team(self):
        return self.team_count() < 5


class Team(models.Model):

    name = models.CharField(max_length=100)
    

    members = models.ManyToManyField(User, related_name='teams')
    

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='teams',  
        null=True,
        blank=True
    )
    
    def add_member(self, user):
        
        if self.members.count() >= 5:
            raise ValueError("Cannot add more than 5 members to a team.")
        
        self.members.add(user)

    def remove_member(self, user):
        if user in self.members.all():
            self.members.remove(user)
        else:
            raise ValueError("User is not a member of this team.")
    
    
    def set_department(self, department):
        
        if department and department.team_count() >= 5:
            raise ValueError(f"Department '{department.name}' already has 5 teams and cannot accept more.")
       
        self.department = department
        self.save()
            
    def __str__(self):
        return self.name

#Employee / Profile to hold the user information    
class Employee(models.Model):
    ROLE_CHOICES = [
        ('engineer', 'Engineer'),
        ('teamleader', 'Team Leader'),
        ('departmentleader', 'Department Leader'),
        ('seniormanager', 'Senior Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
 
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    team_number = models.CharField(max_length=50)
    department_number = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='engineer')
    registered = models.BooleanField(default=False)
 
 
    def __str__(self):
        return self.email