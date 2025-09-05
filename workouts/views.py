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
    parser_classes = [MultiPartParser, FormParser] # Allow image uploads

    pagination_class = PageNumberPagination 
    filter_backends = [DjangoFilterBackend]  # Enable query filtering
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
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Ensure a user can only access their own workouts.
        """
        return Workout.objects.filter(user=self.request.user)
        
    
class AnalyticsGenerateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        today = date.today()
        week_start_date = today - timedelta(days=today.weekday()) # Get Monday of current week

        # Filter workouts for this user and week

        weekly_workouts = Workout.objects.filter(user=user, date__gte=week_start_date)

        if not weekly_workouts.exists():
            return Response({"detail": "No workouts found for this week."}, status=status.HTTP_404_NOT_FOUND)

        # Separate workouts by category for targeted metrics

        strength_workouts = weekly_workouts.filter(category__name="Strength Training")
        cardio_workouts = weekly_workouts.filter(category__name="Cardiovascular Training")

        # Compute total volume: sum of (weight × reps × sets)

        total_volume = strength_workouts.aggregate(
            volume=Sum(F('weight_used') * F('reps') * F('sets'))
        )['volume'] or 0

        # Find max lift from strength workouts

        max_lift = strength_workouts.aggregate(lift=Max('weight_used'))['lift'] or 0

        # Total workout duration across all workouts

        weekly_workout_duration_minutes = weekly_workouts.aggregate(
            duration=Sum('workout_duration_minutes')
        )['duration'] or 0
        
        # Estimate calories burned using MET formula

        total_calories = 0
        user_weight = float(user.weight) if user.weight else 70.0 # Default to 70kg if not set

        for w in weekly_workouts:
            met = 6.0 if w.category.name == "Strength Training" else 7.0
            total_calories += met * 3.5 * user_weight / 200 * w.workout_duration_minutes

        # Compute average intensity 

        intensity = total_volume / weekly_workout_duration_minutes if weekly_workout_duration_minutes > 0 else 0

        # Determine strength level based on max lift vs body weight

        strength_level = "Beginner"
        if max_lift >= 1.5 * user_weight:
            strength_level = "Advanced"
        elif max_lift >= 1.0 * user_weight:
            strength_level = "Intermediate"

        # Prepare analytics data
        analytics_data = {
            'week_start_date': week_start_date,
            'total_volume': total_volume,
            'max_lift': max_lift,
            'average_intensity': round(intensity, 2),
            'strength_level': strength_level,
            'total_calories_burned': round(total_calories, 2),
            'weekly_workout_duration_minutes': weekly_workout_duration_minutes
        }

        # Create or update analytics record for the week

        analytics_record, _ = Analytics.objects.update_or_create(
            user=user,
            week_start_date=week_start_date,
            defaults=analytics_data
        )

        # Return serialized analytics

        serializer = AnalyticsSerializer(analytics_record)
        return Response(serializer.data, status=status.HTTP_200_OK)