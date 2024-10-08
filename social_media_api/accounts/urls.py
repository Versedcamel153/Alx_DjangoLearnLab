from django.urls import path
from .views import RegisterView, UserDetailVIew, LoginView
from .views import FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserDetailVIew.as_view(), name='user-detail'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),#change user_id to pk
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),#change user_id to pk
]
