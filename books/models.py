from django.db import models
from django.conf import settings
from datetime import timedelta, date

class Book(models.Model):
    name = models.CharField(max_length=1000)
    image = models.ImageField(null=True, upload_to='covers')
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200, null=True)
    count = models.SmallIntegerField(default=0)
    
    def remaining_count(self):
        return self.count - Issue.objects.filter(book=self, status=Issue.Status.ISSUED).count()
    
    def __str__(self):
        return f'Name: {self.name}, Author: {self.author}, Remaining: {self.count}'

class Request(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Book: {self.book}, User: {self.user}'

class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_date = models.DateField(null=True)
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        ISSUED = "issued", "Issued"
        RETURNED = "returned", "Returned"
        REJECTED = "rejected", "Rejected"
    status = models.CharField(choices=Status.choices, max_length=9, default=Status.REQUESTED)
    
    @property
    def return_date(self):
        return self.issue_date + timedelta(days=15)
    
    def __str__(self):
        return f'Book: {self.book}, User: {self.user}, return_date: {self.return_date}'