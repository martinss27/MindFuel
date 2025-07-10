from django.urls import path
from .views import GenerateRecommendationsView

urlpatterns = [
    path('generate/', GenerateRecommendationsView.as_view(), name='generate_recommendations'),
]