from rest_framework.permissions import BasePermission
from user.models import User


class IsAdminOrOnlyCreateUser(BasePermission):
    """
    To only allow Admins to create admin or Librarian user
    User role should only b able to create user
    """

    def has_permission(self, request, view):
        """Checks if the current user is an admin or user"""
        user = request.user
        if user.is_authenticated and user.role == User.Role.ADMIN:
            return True
        else:
            try:
                role = request.data.dict()['user.role']
                if role == User.Role.USER:
                    return True
                else:
                    """
                    Specifically adding this to view on browsable api,
                    otherwise it throws an error
                    """
                    return False
            except:
                pass
        return True


class IsAdminOrLibrarian(BasePermission):
    """To check if the requested user is an admin or librarian"""

    def has_permission(self, request, view):
        """Returns boolean depending if the requested user has admin or librarian role"""
        return (request.user.role == User.Role.ADMIN or request.user.role == User.Role.LIBRARIAN)
