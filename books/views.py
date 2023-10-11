from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from books.serializers import BookSerializer, RequestSerializer, TicketSerializer
from books.models import Book, Request, Ticket
from books.permissions import IsLibrarianOrAdminOrReadOnly
from user.models import User
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response


class BooksViewSet(ModelViewSet):
    """
    Viewset to handle all interactions for books
    Librarian and Admin can make all changes but users can only view
    Also allows books to be searched using query parameters based on name
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    # To make sure only Librarian and Admin can make changes
    permission_classes = [IsLibrarianOrAdminOrReadOnly]

    def get_queryset(self):
        """Checks if any search query parameters present and filters accordinglys"""
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        return queryset


class RequestViewSet(ModelViewSet):
    """
    Viewset to handle all interactions for requests
    This includes Request, Issue, Return
    Users can only request books and make no updates
    Librarian and Admins have all permissions
    """
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

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
        # If role is user, only allow request queries
        if role == User.Role.USER:
            serializer.save(status=Request.Status.REQUESTED,
                            user=self.request.user, issue_date=date.today())
        # Otherwise, allow all queries
        else:
            serializer.save(issue_date=date.today())

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
                serializer.save(issue_date=date.today())

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


class TicketViewSet(ModelViewSet):
    """
    Viewset to handle all interactions for Ticket model
    Handles ticket request, accept, reject
    User role can only request and view
    Librarian and Admin have full access
    """
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_queryset(self):
        """If user role, then only show tickets by the user"""
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Create the ticket object and send an email to all librarians"""
        user = self.request.user
        request_data = self.request.data.dict()
        # If role user, create Requested status object and send email to all Librarians
        if user.role == User.Role.USER:
            serializer.save(status=Ticket.Status.REQUESTED)
            librarians = User.objects.filter(role=User.Role.LIBRARIAN).values()
            for librarian in librarians:
                send_mail(
                    "New Book Request Ticket",
                    f'Dear {librarian["username"]},\n'
                    f'User {user.username} has requested a new book to be added\n'
                    f'Requested Book Details:\n'
                    f'Name: {request_data["name"]}\n'
                    f'Author: {request_data["author"]}\n',
                    settings.EMAIL_HOST_USER,
                    [librarian["email"]]
                )
        # Otherwise, save object as requested and send email to all librarians
        else:
            serializer.save()
            # In case update request is sent using PUT
            if ticket["status"] != Ticket.Status.REQUESTED:
                ticket = Ticket.objects.get(
                    user=request_data["user"], name=request_data["name"], author=request_data["author"])
                send_mail(
                    "New Book Request Ticket",
                    f'Dear {ticket.user.username},\n'
                    f'Your request to add the book: \n'
                    f'Name: {ticket.name}\n'
                    f'Author: {ticket.author}\n'
                    f'Has been {ticket.status}',
                    settings.EMAIL_HOST_USER,
                    [ticket.user.email]
                )

    def perform_update(self, serializer):
        """To update fields of Ticket model, mostly status and send subsequent mail to user"""
        user = self.request.user
        # If user role, don't allow action update
        if user.role == User.Role.USER:
            raise PermissionDenied(
                "You are not authorized to perform this action")
        serializer.save()
        request_data = self.request.data.dict()
        # Get ticket from db based on request_data and send mail to user
        ticket = Ticket.objects.get(
            user=request_data["user"], name=request_data["name"], author=request_data["author"])
        send_mail(
            "New Book Request Ticket",
            f'Dear {ticket.user.username},\n'
            f'Your request to add the book: \n'
            f'Name: {ticket.name}\n'
            f'Author: {ticket.author}\n'
            f'Has been {ticket.status}',
            settings.EMAIL_HOST_USER,
            [ticket.user.email]
        )
