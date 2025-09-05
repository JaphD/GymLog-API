from rest_framework import serializers
from .models import UserProfile

# Serializer for creating a new user profile
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
        # Extract profile picture separately

        profile_picture = validated_data.pop('profile_picture', None)

        # Use custom create_user method to ensure password is hashed

        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        
        #  Assign additional profile attributes

        user.height = validated_data.get('height')
        user.weight = validated_data.get('weight')
        user.date_of_birth = validated_data.get('date_of_birth')
        user.gender = validated_data.get('gender')

        # Attach profile picture if provided

        if profile_picture:
            user.profile_picture = profile_picture
            
        user.save()
        return user
    
# Serializer for updating an existing user profile
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

        # Update all other mutable fields

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance