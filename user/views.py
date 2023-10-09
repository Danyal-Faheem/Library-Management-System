from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from user.serializers import UserSerializer, UserProfileSerializer
from user.models import User, UserProfile
from user.permissions import IsAdmin
    
class UserCreateView(CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(role=User.Role.USER)

class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    
    def get_queryset(self):
        return UserProfile.objects.get(user=self.request.user)
    
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    
    
    
