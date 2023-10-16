from django.urls import path, include
from user.views import UserCreateView, UserProfileViewSet
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create', UserCreateView.as_view(), name='create'),
    path('auth', obtain_auth_token, name="auth"),

]
