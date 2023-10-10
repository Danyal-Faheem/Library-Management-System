from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, PermissionDenied
from books.serializers import BookSerializer, RequestSerializer
from books.models import Book, Request
from books.permissions import IsLibrarianOrAdminOrReadOnly
from user.models import User
from datetime import date
class BooksViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsLibrarianOrAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        return queryset


class RequestViewSet(ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()
    permission_classes = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        role = self.request.user.role
        if role == User.Role.USER:
            serializer.save(status=Request.Status.REQUESTED, issue_date=date.today())
        else:
            serializer.save(issue_date=date.today())
            
    
    def perform_update(self, serializer):
        role = self.request.user.role
        if role == User.Role.USER:
            raise PermissionDenied("You are not authorized to perform this action")
        serializer.save()
        status = self.request.data.dict()['status']
        if status is not None:
            if status == Request.Status.ISSUED:
                serializer.save(issue_date=date.today())
            