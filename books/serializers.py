from books.models import Book, Request, Ticket
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book Model"""
    class Meta:
        model = Book
        fields = ['id', 'name', 'image', 'author',
                  'publisher', 'count', 'remaining_count']


class RequestSerializer(serializers.ModelSerializer):
    """Serializer for Request Model"""

    def validate(self, attrs):
        """
        Validates if user has finished their quota of 3 issued books or
        If all copies of the request book are issued or
        User can already requested or issued the requested book
        """
        if attrs['user'].issued_books() >= 3:
            raise serializers.ValidationError(
                "Max issued books at once can't be more than 3.")
        elif attrs['book'].remaining_count() <= 0:
            raise serializers.ValidationError(
                "All copies of this book are currently issued.")
        elif len(Request.objects.filter(user=attrs['user'], book=attrs['book'], status=Request.Status.ISSUED)) > 0 and attrs['status'] == Request.Status.ISSUED:
            raise serializers.ValidationError(
                "Book has already been issued to this user")
        return super().validate(attrs)

    class Meta:
        model = Request
        fields = ['id', 'user', 'book', 'status', 'issue_date', 'return_date']
        # Make issue and return date read only as they are automatically calculated
        extra_kwargs = {
            'issue_date': {'read_only': True},
            'return_date': {'read_only': True},
        }


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket Model"""

    def validate(self, attrs):
        """
        Validates if the requested book is already in the library or
        If the user has already requested this book beforehand
        """
        if len(Book.objects.filter(name=attrs['name'], author=attrs['author'])) > 0 and attrs['status'] == Ticket.Status.REQUESTED:
            raise serializers.ValidationError(
                "This book already exists in the library")
        elif len(Ticket.objects.filter(user=attrs['user'], name=attrs['name'], author=attrs['author'])) > 0 and attrs['status'] == Ticket.Status.REQUESTED:
            raise serializers.ValidationError(
                "You have already Requested this book!")
        return super().validate(attrs)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'name', 'author', 'publisher', 'status']
