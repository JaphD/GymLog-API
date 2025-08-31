from django.urls import path
from .views import (
    WorkoutListCreateView,
    WorkoutDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    AnalyticsGenerateView
)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Workout URLs
    path('', WorkoutListCreateView.as_view(), name='workout-list-create'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='workout-detail'),
    
    # Analytics URLs
    path('analytics/', AnalyticsGenerateView.as_view(), name='analytics-generate'),
]