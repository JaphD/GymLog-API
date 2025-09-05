from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer
from .models import UserProfile
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
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
            # User-related endpoints
            'user_registration': request.build_absolute_uri(reverse('user-register')),
            'user_login': request.build_absolute_uri(reverse('user-login')),
            'user_profile': request.build_absolute_uri(reverse('user-profile')),

            # Workout-related endpoints
            'workouts_list_create': request.build_absolute_uri(reverse('workout-list-create')),
            'workout_detail_example': request.build_absolute_uri(reverse('workout-detail', kwargs={'pk': 1})),
            'categories_list_create': request.build_absolute_uri(reverse('category-list-create')),
            'category_detail_example': request.build_absolute_uri(reverse('category-detail', kwargs={'pk': 1})),
            'analytics_generate': request.build_absolute_uri(reverse('analytics-generate')),

            # Admin-interface
            'admin': request.build_absolute_uri(reverse('admin:index')),
        }
    })

# Handles user registration with public access
class UserRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny] # Open to unauthenticated users
    parser_classes = [MultiPartParser, FormParser] # Support file uploads

# Handles authenticated user profile retrieval and updates
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated] # Only logged-in users can access
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        # Always return the currently authenticated user
        return self.request.user

# Handles logout by blacklisting the refresh token
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the token to invalidate future use
            token = RefreshToken(refresh_token)
            token.blacklist()  # Adds token to blacklist
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            # Handle invalid or expired token errors

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)