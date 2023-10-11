from books.models import Request
from datetime import date
from django.core.mail import send_mail
from django.conf import settings

def return_reminder():
    """"
    Runs at 12am everyday to check whether any issued book is due on that day
    Sends an email reminder to user if book is due on that day
    """
    issued_books = Request.objects.filter(status=Request.Status.ISSUED, return_date=date.today()).values()
    if len(issued_books) > 0:
        for reminder in issued_books:
            send_mail(
                "Book Return Reminder",
                f'The book with the details:\n'
                f'Name: {reminder.book.name}\n'
                f'Author: {reminder.book.author}\n'
                f'should be returned by today!',
                settings.EMAIL_HOST_USER,
                [reminder.user.email],
            )