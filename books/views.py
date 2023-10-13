from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from books.serializers import (
    BookCreateSerializer, BookSerializer, FullRequestSerializer, UserRequestSerializer, ReadRequestSerializer,  ReadTicketSerializer, FullTicketSerializer, UserTicketSerializer)
from books.models import Book, Request, Ticket
from books.permissions import IsLibrarianOrAdminOrReadOnly
from user.models import User
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from LMS.viewset import AuthenticatedModelViewSet


class BooksViewSet(ModelViewSet):
    """
    Viewset to handle all interactions for books
    Librarian and Admin can make all changes but users can only view
    Also allows books to be searched using query parameters based on name
    """
    queryset = Book.objects.all()
    # To make sure only Librarian and Admin can make changes
    permission_classes = [IsLibrarianOrAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Apply different validation checks on book create"""
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookSerializer

    def get_queryset(self):
        """Checks if any search query parameters present and filters accordinglys"""
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        return queryset


class RequestViewSet(AuthenticatedModelViewSet):
    """
    Viewset to handle all interactions for requests
    This includes Request, Issue, Return
    Users can only request books and make no updates
    Librarian and Admins have all permissions
    """
    queryset = Request.objects.all()

    def get_serializer_class(self):
        """To verify user role and method and return respective realizer"""
        role = self.request.user.role
        if self.request.method == 'GET':
            return ReadRequestSerializer
        if role == User.Role.USER:
            return UserRequestSerializer
        return FullRequestSerializer

    def get_queryset(self):
        """If user role, then only show requests by the user"""
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """To create the request object"""
        role = self.request.user.role
        request_data = self.request.data.dict()
        # If role is user, only allow request queries
        if role == User.Role.USER:
            if self.request.user.issued_books() >= 3:
                raise serializers.ValidationError(
                    "Max issued books at once can't be more than 3.")
            elif request_data['book'].remaining_count() <= 0:
                raise serializers.ValidationError(
                    "All copies of this book are currently issued.")
            elif len(Request.objects.filter(user=request_data['user'], book=request_data['book'], status=Request.Status.ISSUED)) > 0:
                raise serializers.ValidationError(
                    "Book has already been issued to this user")
            serializer.save(status=Request.Status.REQUESTED,
                            user=self.request.user)
        # Otherwise, allow all queries
        else:
            if request_data['book'].remaining_count() <= 0:
                raise serializers.ValidationError(
                    "All copies of this book are currently issued.")
            elif len(Request.objects.filter(user=request_data['user'], book=request_data['book'], status=Request.Status.ISSUED)) > 0:
                raise serializers.ValidationError(
                    "Book has already been issued to this user")
            serializer.save()

    def perform_update(self, serializer):
        """Update Request to change status"""
        role = self.request.user.role
        # Do not allow updates to user role
        if role == User.Role.USER:
            raise PermissionDenied(
                "You are not authorized to perform this action")
        serializer.save()
        status = self.request.data.dict()['status']
        # If requested status is to Issue book, update issue_date to current date
        if status is not None:
            if status == Request.Status.ISSUED:
                serializer.save(issue_date=date.today(), return_date=(
                    date.today() + timedelta(days=15)))
            elif status == Request.Status.RETURNED:
                serializer.save(return_date=date.today())

    @action(detail=True, methods=['get'])
    def reminder(self, request, pk=None):
        """ 
        Extra action to manually send reminder to a user about book return
        """
        request = self.get_object()
        send_mail(
            f'Book Return Reminder',
            f'Dear {request.user.username},\n'
            f'You are kindly requested to return the book: \n'
            f'Name: {request.book.name}\n'
            f'Author: {request.book.author}\n'
            f'At the latest by {request.return_date}.\n'
            f'After that, there will be overdue fees which will be calculated per day.\n',
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )
        return Response({"status": "Email Reminder has been sent"})


class TicketViewSet(AuthenticatedModelViewSet):
    """
    Viewset to handle all interactions for Ticket model
    Handles ticket request, accept, reject
    User role can only request and view
    Librarian and Admin have full access
    """
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        """To verify user role and method and return respective realizer"""
        role = self.request.user.role
        if self.request.method == 'GET':
            return ReadTicketSerializer
        if role == User.Role.USER:
            return UserTicketSerializer
        return FullTicketSerializer

    def get_queryset(self):
        """If user role, then only show tickets by the user"""
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Perform validation, else, Create the ticket object and send an email to all librarians"""
        user = self.request.user
        request_data = self.request.data.dict()
        # If role user, create Requested status object and send email to all Librarians
        if user.role == User.Role.USER:
            if len(Book.objects.filter(name=request_data['name'], author=request_data['author'])) > 0:
                raise serializers.ValidationError(
                "This book already exists in the library")
            elif len(Ticket.objects.filter(user=user, name=request_data['name'], author=request_data['author'])) > 0:
                raise serializers.ValidationError(
                "You have already Requested this book!")
            serializer.save(user=user, status=Ticket.Status.REQUESTED)
        # Otherwise, save object as requested and send email to all librarians
        else:
            serializer.save()

    def perform_update(self, serializer):
        """To update fields of Ticket model, mostly status and send subsequent mail to user"""
        user = self.request.user
        # If user role, don't allow action update
        if user.role == User.Role.USER:
            raise PermissionDenied(
                "You are not authorized to perform this action")
        serializer.save()

