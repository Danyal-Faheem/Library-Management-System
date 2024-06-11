from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


class AuthenticatedModelViewSet(ModelViewSet):
    """Inherited ModelViewSet to for views that require authenticated permissions and classes"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
