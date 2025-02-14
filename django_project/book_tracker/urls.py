from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

from . import views
from .views import search_results

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('posts/', PostListView.as_view(), name='post-list'),  # Separate URL for posts
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('search/', views.search_results, name='search_results'),  # search bar
    path('posts/',views.posts, name='blog-posts'),
    path('inbox/', include('inbox.urls')),
    path('users/', include('users.urls')),  # Include user-related URLs
]