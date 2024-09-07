from rest_framework import serializers
from .models import Book, Author
from datetime import date
class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer:
    This serializer serializes all fileds of the book model.
    It ensures that all attributes(title, author, book) are included in the serialization process.
    It also includes custom validation to ensure the publication year is not set to the future.
    """
    class Meta:
        model = Book
        fields = '__all__' # Include all fields in the serialization

    def validate_publication_year(Self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer:
    This serializer serilizes the name field of the Author model.
    It also includes a nested BookSerialzer to dynamically serialize related book.
    The 'books' fields is a read-only field that uses the BookSerializer to include detailed information about each book written by the author.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
