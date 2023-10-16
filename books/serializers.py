from books.models import Book, Request, Ticket
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book Model"""
    class Meta:
        model = Book
        fields = ['id', 'name', 'image', 'author',
                  'publisher', 'count']


class BookCreateSerializer(serializers.ModelSerializer):
    """Serializer for Book Model"""

    def validate(self, attrs):
        if len(Book.objects.filter(name=attrs['name'], author=attrs['author'], publisher=attrs['publisher'])) > 0:
            raise serializers.ValidationError(
                "This book already exists in the library!")
        return super().validate(attrs)

    class Meta:
        model = Book
        fields = ['id', 'name', 'image', 'author',
                  'publisher', 'count', 'remaining_count']
        read_only_fields = ['remaining_count']


class FullRequestSerializer(serializers.ModelSerializer):
    """Serializer for Request Model that allows all actions"""

    class Meta:
        model = Request
        fields = ['id', 'user', 'book', 'status', 'issue_date', 'return_date']
        # Make issue and return date read only as they are automatically calculated
        read_only_fields = ['issue_date', 'return_date']


class ReadRequestSerializer(serializers.ModelSerializer):
    """Serializer to only allow read access to Request Model"""
    class Meta:
        model = Request
        fields = ['id', 'user', 'book', 'status', 'issue_date', 'return_date']
        # Make all fields read_only
        read_only_fields = fields


class UserRequestSerializer(serializers.ModelSerializer):
    """Serializer for Requests allowed to the User"""

    class Meta:
        model = Request
        fields = ['id', 'user', 'book', 'status']
        # Don't allow user to change User and Status
        read_only_fields = ['user', 'status']


class FullTicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket Model"""

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'name', 'author', 'publisher', 'status']


class ReadTicketSerializer(serializers.ModelSerializer):
    """Serializer to only allow read access to Ticket Model"""
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'name', 'author', 'publisher', 'status']
        read_only_fields = fields


class UserTicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket Model"""

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'name', 'author', 'publisher', 'status']
        read_only_fields = ['user', 'status']
