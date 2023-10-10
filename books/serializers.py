from books.models import Book, Request, Request
from rest_framework import serializers
from user.serializers import UserSerializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'image', 'author', 'publisher', 'count', 'remaining_count']
        

class RequestSerializer(serializers.ModelSerializer):
    
    def validate(self, attrs):
        if attrs['user'].issued_books() >= 3:
            raise serializers.ValidationError("Max issued books at once can't be more than 3.")
        elif attrs['book'].remaining_count() <= 0:
            raise serializers.ValidationError("All books are currently issued.")
        elif len(Request.objects.filter(user=attrs['user'], book=attrs['book'], status=Request.Status.ISSUED)) > 0 and attrs['status'] == Request.Status.ISSUED:
            raise serializers.ValidationError("Book has already been issued to this user")
        return super().validate(attrs)
    class Meta:
        model = Request
        fields = ['id', 'user', 'book', 'status', 'issue_date', 'return_date']
        extra_kwargs = {
            'issue_date': {'read_only': True},
            'return_date': {'read_only': True},
        }