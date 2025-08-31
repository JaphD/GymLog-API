import django_filters
from .models import Workout

class WorkoutFilter(django_filters.FilterSet):
    # Allow filtering by date and a date range
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    date_after = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    
    # Allow case-insensitive search on exercise name
    exercise_name = django_filters.CharFilter(field_name='exercise_name', lookup_expr='icontains')
    
    class Meta:
        model = Workout
        fields = ['date', 'date_after', 'date_before', 'exercise_name']