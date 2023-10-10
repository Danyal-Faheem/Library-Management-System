from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from user.serializers import UserSerializer, UserProfileSerializer
from user.models import User, UserProfile
from user.permissions import IsAdminOrLibrarian
from rest_framework.response import Response
from rest_framework import status
    
class UserCreateView(CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    
    def list(self, request, *args, **kwargs):
        # if request.user.role == User.Role.USER:
        #     response = {'message': 'You are not authorized to use this function'}
        #     return Response(response, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)
    
    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    
    
