from django.urls import path
from .views import GenerateLearningPathView

urlpatterns = [
    path('generate/', GenerateLearningPathView.as_view(), name='generate_learning_path'),
]