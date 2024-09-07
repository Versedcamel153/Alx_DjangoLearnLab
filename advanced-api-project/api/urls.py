from django.urls import path
from .views import BookListCreateAPIView, BookDeleteView, BookRetrieveUpdateDestroyAPIView, BookCreateView, BookUpdateView, BookDetailView


urlpatterns = [
    path('', BookListCreateAPIView.as_view(), name='book_list_create_api'),
    path('<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book_detail_update_delete_api'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('new/', BookCreateView.as_view(), name='book_create'),
]