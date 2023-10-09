from django.urls import path, include
from user.views import UserCreateView, UserProfileViewSet, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create', UserCreateView.as_view(), name='create'),

]
