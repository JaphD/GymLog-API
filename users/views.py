from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer
from .models import UserProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse

@api_view(['GET'])
def api_root(request, format=None):
    """
    Root API endpoint listing all accessible URLs dynamically.
    """
    return Response({
        'message': 'Welcome to GymLog API',
        'status': 'OK',
        'version': '1.0.0',
        'endpoints': {
            # Users app
            'user_registration': request.build_absolute_uri(reverse('user-register')),
            'user_login': request.build_absolute_uri(reverse('user-login')),
            'user_profile': request.build_absolute_uri(reverse('user-profile')),

            # Workouts app
            'workouts_list_create': request.build_absolute_uri(reverse('workout-list-create')),
            'workout_detail_example': request.build_absolute_uri(reverse('workout-detail', kwargs={'pk': 1})),
            'categories_list_create': request.build_absolute_uri(reverse('category-list-create')),
            'category_detail_example': request.build_absolute_uri(reverse('category-detail', kwargs={'pk': 1})),
            'analytics_generate': request.build_absolute_uri(reverse('analytics-generate')),

            # Admin
            'admin': request.build_absolute_uri(reverse('admin:index')),
        }
    })

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user