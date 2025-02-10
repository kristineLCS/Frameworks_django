from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views
from .views import book_search

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('posts/', PostListView.as_view(), name='post-list'),  # Separate URL for posts
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('search/', views.book_search, name='book_search'),  # search bar
    path('posts/',views.posts, name='blog-posts'),
]