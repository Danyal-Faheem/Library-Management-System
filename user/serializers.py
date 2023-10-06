from rest_framework import serializers
from user.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'role', 'issued_books']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone_number', 'gender']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
