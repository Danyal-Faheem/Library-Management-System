from rest_framework.permissions import BasePermission
from user.models import User


class IsLibrarianOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (request.user.role == User.Role.ADMIN or request.user.role == User.Role.LIBRARIAN)
