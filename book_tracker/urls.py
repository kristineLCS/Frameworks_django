from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from .views import post_announcement, AnnouncementCreateView, AnnouncementUpdateView, AnnouncementDeleteView
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post-announcement/', post_announcement, name='post_announcement'),
    path('announcement/new/', AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcement/edit/<int:pk>/', AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcement/delete/<int:pk>/', AnnouncementDeleteView.as_view(), name='announcement_delete'),
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