from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile_view'),
    path('home/', HomeView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/comments/new/', PostDetailView.as_view(), name='add_comment'),
    path('posts/<int:pk>/comments/edit/', CommentEditView.as_view(), name='edit_comment'),
    path('posts/<int:pk>/comments/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('search/', search_view, name='search'),
    path('tags/<slug:slug>/', tagged_posts_view, name='tagged_posts')
]