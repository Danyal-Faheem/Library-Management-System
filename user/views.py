from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from user.serializers import UserProfileSerializer
from user.models import User, UserProfile
from rest_framework.response import Response
from rest_framework import status


class UserCreateView(CreateAPIView):
    """View to create a userprofile and user together"""
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserProfileViewSet(ModelViewSet):
    """
    Viewset to handle all tasks related to user profile
    Create functionality is disabled
    User role can only manage their own profile
    Admin and Librarian can manage all profiles
    """
    serializer_class = UserProfileSerializer
    # To make sure only authenticated users can access
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        """If user role, only allow users own profile"""
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset


    def list(self, request, *args, **kwargs):
        """Overriding list to only return single userprofile object"""
        if request.user.role == User.Role.USER:
            response = UserProfileSerializer(UserProfile.objects.get(user=request.user)).data
            return Response(response, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Create function is disabled as that has a separate route to allow
        non authenticated users to sign up as well
        """
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
