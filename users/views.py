from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserProfile

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
     # The registration view needs parsers to handle form data and JSON.
    parser_classes = [MultiPartParser, FormParser]

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    # The profile view needs these parsers to handle file uploads and form data.
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user