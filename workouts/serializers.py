from rest_framework import serializers
from .models import Workout, Category, Analytics

# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name'] # Minimal fields for listing and creation

# Serializer for Workout model
class WorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for the Workout model.
    """
    category_name = serializers.CharField(source='category.name', read_only=True) # Exposes category name

    class Meta:
        model = Workout
        fields = [
            'id', 'user', 'exercise_name', 'weight_used', 'reps', 'sets', 
            'date', 'notes', 'image', 'category', 'category_name',
            'workout_duration_minutes'
        ]
        read_only_fields = ['user', 'category_name']  # User is set from request context; category_name is derived

# Serializer for Analytics model
class AnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Analytics model."""
    class Meta:
        model = Analytics
        fields = [
            'id', 'user', 'week_start_date', 'total_volume', 
            'max_lift', 'average_intensity', 'strength_level', 'total_calories_burned', 'weekly_workout_duration_minutes'
        ]
        read_only_fields = [
            'user', 'total_volume', 'max_lift', 'average_intensity', 'strength_level',
            'total_calories_burned', 'weekly_workout_duration_minutes'
        ] # All fields except user and week_start_date are computed