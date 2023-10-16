from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from books.models import Ticket
from user.models import User
from django.conf import settings


@receiver(post_save, sender=Ticket)
def send_email_on_status_change(sender, instance, created, **kwargs):
    if not created:
        send_mail(
            "New Book Request Ticket",
            f'Dear {instance.user.username},\n'
            f'Your request to add the book: \n'
            f'Name: {instance.name}\n'
            f'Author: {instance.author}\n'
            f'Has been {instance.status}',
            settings.EMAIL_HOST_USER,
            [instance.user.email]
        )


@receiver(post_save, sender=Ticket)
def send_email_on_create(sender, instance, created, **kwargs):
    if created:
        librarians = User.objects.filter(role=User.Role.LIBRARIAN).values()
        for librarian in librarians:
            send_mail(
                "New Book Request Ticket",
                f'Dear {librarian["username"]},\n'
                f'User {instance.user.username} has requested a new book to be added\n'
                f'Requested Book Details:\n'
                f'Name: {instance.name}\n'
                f'Author: {instance.author}\n',
                settings.EMAIL_HOST_USER,
                [librarian["email"]]
            )
