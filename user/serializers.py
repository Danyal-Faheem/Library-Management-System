from rest_framework import serializers
from user.models import User, UserProfile
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'role', 'issued_books']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'issued_books': {'read_only': True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'gender']
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(password=make_password(password), role=User.Role.USER, **user_data)
        return UserProfile.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        user = instance.user
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        user.username = validated_data.get('username', user.username)
        user.email = validated_data.get('email', user.email)
        user.save()
        
