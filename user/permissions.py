from rest_framework.permissions import BasePermission
from user.models import User

class IsAdminOrOnlyCreateUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if  user.is_authenticated and user.role == User.Role.ADMIN:
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
    def has_permission(self, request, view):
        return (request.user.role == User.Role.ADMIN or request.user.role == User.Role.LIBRARIAN)