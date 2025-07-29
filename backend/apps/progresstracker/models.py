from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    milestone = models.ForeignKey('milestone', on_delete=models.CASCADE)
    created_by_AI = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=50, choices=[
        ('multiple_choice', 'multiple_choice'),
        ('true_false', 'true_false'),
        ('fill_in_the_blank', 'fill_in_the_blank')
    ])

class Answer(models.Model):
    question = models.ForeignKey(Question,related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)