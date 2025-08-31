# workouts/models.py

from django.db import models
from django.conf import settings

class Category(models.Model):
    """
    Model to group exercises (e.g., 'Cardio', 'Strength', 'Yoga').
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    """
    Model for a single workout session entry.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workouts'
    )
    exercise_name = models.CharField(max_length=255)
    weight_used = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reps = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)
    workout_duration_minutes = models.PositiveIntegerField(default=0)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='workout_images/', null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='workouts',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'exercise_name']

    def __str__(self):
        return f"{self.user.username}'s {self.exercise_name} on {self.date}"

class Analytics(models.Model):
    """
    Model to store weekly workout analytics.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    week_start_date = models.DateField(unique=True)
    total_volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_lift = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    strength_level = models.CharField(max_length=50, default='Beginner')
    total_calories_burned = models.PositiveIntegerField(default=0)
    workout_duration_minutes = models.PositiveIntegerField(default=0) # Add this line

    class Meta:
        ordering = ['-week_start_date']

    def __str__(self):
        return f"{self.user.username}'s analytics for week starting {self.week_start_date}"