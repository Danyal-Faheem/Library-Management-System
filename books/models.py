from django.db import models
from django.conf import settings
from datetime import timedelta, date


class Book(models.Model):
    """Book model which contains the main book object"""
    name = models.CharField(max_length=1000)
    image = models.ImageField(null=True, upload_to='covers')
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, null=True)
    count = models.SmallIntegerField(default=0)

    def remaining_count(self):
        """Returns the number of books currently not issued in inventory"""
        return self.count - Request.objects.filter(book=self, status=Request.Status.ISSUED).count()

    def __str__(self):
        return f'Name: {self.name}, Author: {self.author}, Remaining: {self.count}'


class Request(models.Model):
    """To handle the request, issue and return of books"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    issue_date = models.DateField(null=True)

    class Status(models.TextChoices):
        """
        Status of each request, changed to depict the current status
        Utilized TextChoices here as I required some comparisons with keys using request data
        """
        REQUESTED = "requested", "Requested"
        ISSUED = "issued", "Issued"
        RETURNED = "returned", "Returned"
        REJECTED = "rejected", "Rejected"
    status = models.CharField(choices=Status.choices,
                              max_length=9, default=Status.REQUESTED)

    @property
    def return_date(self):
        """Auto calculates the return date which is 15 days after issue_date"""
        return self.issue_date + timedelta(days=15)

    def __str__(self):
        return f'Book: {self.book}, User: {self.user}, return_date: {self.return_date}'


class Ticket(models.Model):
    """To handle the request, accept and reject of each new book ticket"""
    name = models.CharField(max_length=1000)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    class Status(models.TextChoices):
        """
        Status of each request, changed to depict the current status
        Utilized TextChoices here as I required some comparisons with keys using request data
        """
        REQUESTED = "requested", "Requested"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
    status = models.CharField(choices=Status.choices,
                              max_length=9, default=Status.REQUESTED)

    def __str__(self):
        return f'User: {self.user}\nName: {self.name}, Author: {self.author}'
