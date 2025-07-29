from django.db import models
from django.conf import settings

class Habit(models.Model):
    LEVEL_CHOICES = [
        ('easy', 'easy'),
        ('mid', 'mid'),
        ('intense', 'intense'), 
    ]
    STATUS_CHOICES = [
        ('in_progress', 'in progress'),
        ('done', 'done'),
        ('ignored', 'ignored'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')


    def __str__(self): 
        # type: ignore[attr-defined]
        return f"{self.name} ({self.get_level_display()}) - {self.user.username}"