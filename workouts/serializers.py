from rest_framework import serializers
from .models import Workout, Category, Analytics

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']

class WorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for the Workout model.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Workout
        fields = [
            'id', 'user', 'exercise_name', 'weight_used', 'reps', 'sets', 
            'date', 'notes', 'image', 'category', 'category_name',
            'workout_duration_minutes'
        ]
        read_only_fields = ['user', 'category_name']

class AnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Analytics model."""
    class Meta:
        model = Analytics
        fields = [
            'id', 'user', 'week_start_date', 'total_volume', 
            'max_lift', 'strength_level', 'total_calories_burned', 'workout_duration_minutes'
        ]
        read_only_fields = [
            'user', 'total_volume', 'max_lift', 'strength_level',
            'total_calories_burned'
        ]