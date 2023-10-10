from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from books.serializers import BookSerializer, RequestSerializer, TicketSerializer
from books.models import Book, Request, Ticket
from books.permissions import IsLibrarianOrAdminOrReadOnly
from user.models import User
from datetime import date
from django.core.mail import send_mail
from django.conf import settings


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

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        role = self.request.user.role
        if role == User.Role.USER:
            serializer.save(status=Request.Status.REQUESTED,
                            issue_date=date.today())
        else:
            serializer.save(issue_date=date.today())

    def perform_update(self, serializer):
        role = self.request.user.role
        if role == User.Role.USER:
            raise PermissionDenied(
                "You are not authorized to perform this action")
        serializer.save()
        status = self.request.data.dict()['status']
        if status is not None:
            if status == Request.Status.ISSUED:
                serializer.save(issue_date=date.today())


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.user.role
        if role == User.Role.USER:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        request_data = self.request.data.dict()
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
        else:
            serializer.save()
            if ticket["status"] != Ticket.Status.REQUESTED:
                ticket = Ticket.objects.get(user=request_data["user"], name=request_data["name"], author=request_data["author"])
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
        user = self.request.user
        if user.role == User.Role.USER:
            raise PermissionDenied(
                "You are not authorized to perform this action")
        serializer.save()
        request_data = self.request.data.dict()
        ticket = Ticket.objects.get(user=request_data["user"], name=request_data["name"], author=request_data["author"])
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
