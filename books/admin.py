from django.contrib import admin
from books.models import Book, Request, Issue

admin.site.register(Book)
admin.site.register(Request)
admin.site.register(Issue)
