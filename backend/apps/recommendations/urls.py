from django.urls import path
from .views import (
    GenerateRecommendationsView,
    UserHabitListCreateView,
    UserHabitUpdateView,
    UserHabitDeleteView,
)
urlpatterns = [
    path('generate/', GenerateRecommendationsView.as_view(), name='generate_recommendations'),
    path('user-habits/', UserHabitListCreateView.as_view(), name='user_habit_list_create'),
    path('user-habits/<int:pk>/', UserHabitUpdateView.as_view(), name='user_habit_update'),
    path('user-habits/<int:pk>/delete/', UserHabitDeleteView.as_view(), name='user_habit_delete'),
]