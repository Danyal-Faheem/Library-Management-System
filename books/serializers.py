from books.models import Book, Request, Issue
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'image', 'author', 'publisher', 'count', 'remaining_count']
        

class IssueSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['user'].issued_books() >= 3:
            raise serializers.ValidationError("Max issued books at once can't be more than 3.")
        elif attrs['book'].remaining_count() <= 0:
            raise serializers.ValidationError("All books are currently issued.")
        return super().validate(attrs)
    class Meta:
        model = Issue
        fields = ['id', 'user', 'book', 'status', 'issue_date', 'return_date']
        extra_kwargs = {
            'issue_date': {'read_only': True},
            'return_date': {'read_only': True}, 
            'status': {'read_only': True}
        }