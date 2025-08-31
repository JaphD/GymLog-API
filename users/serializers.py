from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    age = serializers.ReadOnlyField() # To display the calculated age

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'height', 'weight', 'date_of_birth', 'gender', 'profile_picture', 'age'
        )
        read_only_fields = ('id', 'age')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        # Update extra fields
        user.height = validated_data.get('height')
        user.weight = validated_data.get('weight')
        user.date_of_birth = validated_data.get('date_of_birth')
        user.gender = validated_data.get('gender')
        user.save()
        return user
    
# users/serializers.py
# ... other imports and your current UserProfileSerializer

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'height', 'weight', 'date_of_birth', 'gender', 'profile_picture', 'age'
        )
        read_only_fields = ('id', 'username', 'email', 'age')
        
    def update(self, instance, validated_data):
        # Handle profile picture update separately
        profile_picture = validated_data.pop('profile_picture', None)
        if profile_picture:
            instance.profile_picture = profile_picture

        # Call the parent update method for other fields
        return super().update(instance, validated_data)