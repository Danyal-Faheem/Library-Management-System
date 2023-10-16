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

    # def validate(self, attrs):
    #     """
    #     Validates if user has finished their quota of 3 issued books or
    #     If all copies of the request book are issued or
    #     User can already requested or issued the requested book
    #     """
    #     if attrs['user'].issued_books() >= 3:
    #         raise serializers.ValidationError(
    #             "Max issued books at once can't be more than 3.")
    #     elif attrs['book'].remaining_count() <= 0:
    #         raise serializers.ValidationError(
    #             "All copies of this book are currently issued.")
    #     elif len(Request.objects.filter(user=attrs['user'], book=attrs['book'], status=Request.Status.ISSUED)) > 0 and attrs['status'] == Request.Status.ISSUED:
    #         raise serializers.ValidationError(
    #             "Book has already been issued to this user")
    #     return super().validate(attrs)

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

    # def validate(self, attrs):
    #     """
    #     Validates if user has finished their quota of 3 issued books or
    #     If all copies of the request book are issued or
    #     User can already requested or issued the requested book
    #     """
    #     print(attrs)
    #     if self.request.user.issued_books() >= 3:
    #         raise serializers.ValidationError(
    #             "Max issued books at once can't be more than 3.")
    #     elif attrs['book'].remaining_count() <= 0:
    #         raise serializers.ValidationError(
    #             "All copies of this book are currently issued.")
    #     elif len(Request.objects.filter(user=attrs['user'], book=attrs['book'], status=Request.Status.ISSUED)) > 0 and attrs['status'] == Request.Status.ISSUED:
    #         raise serializers.ValidationError(
    #             "Book has already been issued to this user")
    #     return super().validate(attrs)

    class Meta:
        model = Request
        fields = ['id', 'user', 'book', 'status']
        # Don't allow user to change User and Status
        read_only_fields = ['user', 'status']


class FullTicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket Model"""

    # def validate(self, attrs):
    #     """
    #     Validates if the requested book is already in the library or
    #     If the user has already requested this book beforehand
    #     """
    #     if len(Book.objects.filter(name=attrs['name'], author=attrs['author'])) > 0 and attrs['status'] == Ticket.Status.REQUESTED:
    #         raise serializers.ValidationError(
    #             "This book already exists in the library")
    #     elif len(Ticket.objects.filter(user=attrs['user'], name=attrs['name'], author=attrs['author'])) > 0 and attrs['status'] == Ticket.Status.REQUESTED:
    #         raise serializers.ValidationError(
    #             "You have already Requested this book!")
    #     return super().validate(attrs)

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

    # def validate(self, attrs):
    #     """
    #     Validates if the requested book is already in the library or
    #     If the user has already requested this book beforehand
    #     """
    #     if len(Book.objects.filter(name=attrs['name'], author=attrs['author'])) > 0 and attrs['status'] == Ticket.Status.REQUESTED:
    #         raise serializers.ValidationError(
    #             "This book already exists in the library")
    #     elif len(Ticket.objects.filter(user=attrs['user'], name=attrs['name'], author=attrs['author'])) > 0 and attrs['status'] == Ticket.Status.REQUESTED:
    #         raise serializers.ValidationError(
    #             "You have already Requested this book!")
    #     return super().validate(attrs)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'name', 'author', 'publisher', 'status']
        read_only_fields = ['user', 'status']
