from rest_framework import serializers
from user.models import User, UserProfile
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User Model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'role', 'issued_books']
        """
        Making Password as write_only for security
        Role is read_only as default role is user
        Only admin can change role from admin panel
        Issued_books cannot be changed as it is calculated
        """
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'issued_books': {'read_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'gender']

    def create(self, validated_data):
        """
        Overriden create method to create user object as well
        Creates user object with role as USER
        Also creates UserProfile object with request data
        """
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(password=make_password(
            password), role=User.Role.USER, **user_data)
        return UserProfile.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        """Overriden update method to update user model fields as well"""
        user = instance.user
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get(
            'phone_number', instance.phone_number)
        user.username = validated_data.get('username', user.username)
        user.email = validated_data.get('email', user.email)
        user.save()
