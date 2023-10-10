from rest_framework.permissions import BasePermission
from user.models import User


class IsLibrarianOrAdminOrReadOnly(BasePermission):
    """
    Permission to make sure only Librarian or Admin role can make changes
    However, user role can still view data
    All users must be authenticated
    """

    def has_permission(self, request, view):
        """If a request to view, allow all authenticated users but check for permissions otherwise."""
        if request.method == 'GET':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (request.user.role == User.Role.ADMIN or request.user.role == User.Role.LIBRARIAN)
