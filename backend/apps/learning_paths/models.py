from django.db import models
from django.conf import settings

class LearningPath(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_paths')
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Step(models.Model):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField()