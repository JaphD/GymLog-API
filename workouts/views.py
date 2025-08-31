# workouts/views.py

from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser # Add JSONParser
from .models import Workout, Category, Analytics
from rest_framework.views import APIView
from datetime import date, timedelta
from django.db.models import Sum, Max, F
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkoutSerializer, CategorySerializer, AnalyticsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import WorkoutFilter

# Category Views 
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all workout categories or create a new one.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Workout Views 
class WorkoutListCreateView(generics.ListCreateAPIView):
    """
    List all workouts for the authenticated user or to create a new workout.
    """
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    pagination_class = PageNumberPagination 
    filter_backends = [DjangoFilterBackend]  # Add this line
    filterset_class = WorkoutFilter

    def get_queryset(self):
        """
        Filter the queryset to return only the workouts for the authenticated user.
        """
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Set the user for the workout before saving.
        """
        serializer.save(user=self.request.user)

class WorkoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific workout.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        """
        Ensure a user can only access their own workouts.
        """
        return Workout.objects.filter(user=self.request.user)
        
    
class AnalyticsGenerateView(APIView):
    """
    Generate and retrieve weekly analytics for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        today = date.today()
        week_start_date = today - timedelta(days=today.weekday())

        # Aggregate all workouts for the current week
        weekly_workouts = Workout.objects.filter(
            user=user,
            date__gte=week_start_date
        )

        # Calculate metrics using Django's ORM
        total_volume = weekly_workouts.aggregate(
            volume=Sum(F('weight_used') * F('reps') * F('sets'))
        )['volume'] or 0

        max_lift = weekly_workouts.aggregate(
            lift=Max('weight_used')
        )['lift'] or 0

        workout_duration_minutes = weekly_workouts.aggregate(
            duration=Sum('workout_duration_minutes')
        )['duration'] or 0
        
        # Simple placeholder for calories burned
        total_calories_burned = weekly_workouts.aggregate(
            calories=Sum(
                F('workout_duration_minutes') * F('category__met_value') * 3.5 * F('user__userprofile__weight') / 200
            )
        )['calories'] or 0
        
        strength_level = 'Beginner'
        if total_volume > 10000:
            strength_level = 'Advanced'
        elif total_volume > 5000:
            strength_level = 'Intermediate'
        
        
        # Prepare the data to be saved or returned
        analytics_data = {
            'user': user.id,
            'week_start_date': week_start_date,
            'total_volume': total_volume,
            'max_lift': max_lift,
            'strength_level': strength_level,
            'total_calories_burned': total_calories_burned,
            'workout_duration_minutes': workout_duration_minutes,
        }

        # Check if an analytics record for the week already exists
        # If it does, update it; otherwise, return the data without saving
        try:
           analytics_record, _ = Analytics.objects.update_or_create(
            user=user,
            week_start_date=week_start_date,
            defaults={
                'total_volume': total_volume,
                'max_lift': max_lift,
                'strength_level': strength_level,
                'total_calories_burned': total_calories_burned,
                'workout_duration_minutes': workout_duration_minutes,
            }
        )
        except Analytics.DoesNotExist:
            serializer = AnalyticsSerializer(data=analytics_data)
            serializer.is_valid(raise_exception=True)
        
        serializer = AnalyticsSerializer(analytics_record)
        return Response(serializer.data, status=status.HTTP_200_OK)