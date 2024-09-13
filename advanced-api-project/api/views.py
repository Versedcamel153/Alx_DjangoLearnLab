from django.shortcuts import render
from rest_framework import generics, permissions, filters
from django.urls import reverse_lazy
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import DeleteView, DetailView, CreateView, UpdateView, ListView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .filters import BookFilter
from .models import Book
from .forms import BookForm
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly

# API Views
class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve list of books or create a new book.
    
    - GET: Allow any user (authenticated or not) to view the list of books.
    - POST: Only authenticated users can create a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'author__name', 'publication_year']
    ordering = ['title']  # Default ordering
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """
        Customize permissions based on request method.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

# Django Views
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/delete_book.html'
    success_url = reverse_lazy('book_list')
