from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend

class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve list of books or create new book.
    
    - GET: Allow any user (authenticated or not) to view the list of books.
    - POST: Only authenticated users can create a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Customize permissions based on request method.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a book by ID.
    
    - GET: Allow any user (authenticated or not) to view book details.
    - PUT, PATCH, DELETE: Only authenticated users can modify or delete the book.
    """
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Customize permissions based on request method.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]