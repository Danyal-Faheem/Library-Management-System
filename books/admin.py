from django.contrib import admin
from books.models import Book, Request, Ticket

admin.site.register(Book)
admin.site.register(Request)
admin.site.register(Ticket)
