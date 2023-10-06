from django.urls import path
from user.views import UserCreateView, UserProfileListUpdateDeleteView, UserViewSet

urlpatterns = [
    path('list', UserViewSet.as_view(
        {"get": "list", "post": "update", "patch": "partial_update", "delete": "destroy"}), name='list'),
    path('create', UserCreateView.as_view(), name='create'),
    path('profile', UserProfileListUpdateDeleteView.as_view(
        {"get": "retrieve", "post": "update", "patch": "partial_update", "delete": "destroy"}), name='profile')
]
