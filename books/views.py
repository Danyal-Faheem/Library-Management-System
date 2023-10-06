from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from books.serializers import BookSerializer, IssueSerializer
from books.models import Book, Issue
from books.permissions import IsLibrarianOrAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from user.models import User
from rest_framework.response import Response
from rest_framework import status
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


class RequestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    serializer_class = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user, status=Issue.Status.REQUESTED)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(status=Issue.Status.REQUESTED)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsLibrarianOrAdminOrReadOnly]

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        serializer.save(status=Issue.Status.ISSUED,
                        issue_date=date.today())

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user, status=Issue.Status.ISSUED)
        return queryset


class ReturnViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsLibrarianOrAdminOrReadOnly]

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        serializer.save(status=Issue.Status.RETURNED,
                        return_date=date.today())

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user, status=Issue.Status.RETURNED)
        return queryset

class RejectViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [IsLibrarianOrAdminOrReadOnly]

    def create(self, request):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        serializer.save(status=Issue.Status.REJECTED)

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user, status=Issue.Status.REJECTED)
        return queryset