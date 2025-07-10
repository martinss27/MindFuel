from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'user', 'name', 'description', 'level', 'status']
        read_only_fields = ['id', 'user']

    def create(self,validated_data):
        user = self.context['request'].user
        return Habit.objects.create(user=user, **validated_data)