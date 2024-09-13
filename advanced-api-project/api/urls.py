from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    BookDetailView
)

urlpatterns = [
    # API URLs
    path('books/', BookListCreateAPIView.as_view(), name='book_list_create_api'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book_detail_update_delete_api'),
    
    # Django views URLs
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/update/', BookUpdateView.as_view(), name='book_update'),
    path('books/delete/', BookDeleteView.as_view(), name='book_delete'),
]
