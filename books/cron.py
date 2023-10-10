from books.models import Request
from datetime import date
from django.core.mail import send_mail
from django.conf import settings

def return_reminder():
    issued_books = Request.objects.filter(status=Request.Status.ISSUED)
    if issued_books is not None:
        reminders = [reminder for reminder in issued_books if reminder.return_date == date.today()]
        for reminder in reminders:
            send_mail(
                "Book Return Reminder",
                f'The book with the details:\n'
                f'Name: {reminder.book.name}\n'
                f'Author: {reminder.book.author}\n'
                f'should be returned by today!',
                settings.EMAIL_HOST_USER,
                [reminder.user.email],
            )