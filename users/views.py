from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer
from .models import UserProfile
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'Welcome to GymLog API',
        'status': 'OK',
        'version': '1.0.0',
        'endpoints': {
            'users': request.build_absolute_uri('api/users/'),
            'workouts': request.build_absolute_uri('api/workouts/'),
            'admin': request.build_absolute_uri('admin/'),
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