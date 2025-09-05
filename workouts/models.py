# workouts/models.py

from django.db import models
from django.conf import settings

class Category(models.Model):
    """
    Model to group exercises ('Strength Training' and 'Cardiovascular Training').
    """
    name = models.CharField(max_length=255, unique=True) # Ensure category names are distinct


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
    weight_used = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) # e.g., 120.50 kg

    reps = models.PositiveIntegerField(null=True, blank=True)
    sets = models.PositiveIntegerField(null=True, blank=True)
    workout_duration_minutes = models.PositiveIntegerField(default=0) # Total time spent

    date = models.DateField() # Workout date

    notes = models.TextField(blank=True, null=True) # Optional user notes

    image = models.ImageField(upload_to='workout_images/', null=True, blank=True) # Optional image upload

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # Preserve workout if category is deleted
        related_name='workouts',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True) # Timestamp for creation

    updated_at = models.DateTimeField(auto_now=True) # Timestamp for last update

    class Meta:
        ordering = ['-date', 'exercise_name'] # Recent workouts first

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
    week_start_date = models.DateField() # Start of the tracked week

    # Aggregated metrics
    total_volume = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Sum of (weight × reps × sets)

    max_lift = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Heaviest lift recorded

    average_intensity = models.DecimalField(max_digits=8, decimal_places=2, default=0) # Custom intensity metric

    strength_level = models.CharField(max_length=50, default='Beginner') # Computed level

    total_calories_burned = models.PositiveIntegerField(default=0)
    weekly_workout_duration_minutes = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['-week_start_date'] # Show most recent analytics first

        constraints = [
            models.UniqueConstraint(fields=['user', 'week_start_date'], name='unique_analytics_per_user_per_week') # Prevent duplicate entries per week

        ]

    def __str__(self):
        return f"{self.user.username}'s analytics for week starting {self.week_start_date}"