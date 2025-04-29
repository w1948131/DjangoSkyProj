from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class HealthCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Health Card {self.user.username} - {self.created_at.date()}"

class Vote(models.Model):
    COLOR_CHOICES = [
        (1, 'Red'),
        (2, 'Amber'),
        (3, 'Green'),
    ]

    health_card = models.ForeignKey(HealthCard, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    color = models.IntegerField(choices=COLOR_CHOICES)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['health_card', 'category']

    def get_color_display_name(self):
        return dict(self.COLOR_CHOICES)[self.color]