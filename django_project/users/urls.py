from django.urls import path
from . import views
from .views import (
    add_book_to_folder, 
    create_folder,
    FolderListView, 
    FolderCreateView, 
    FolderUpdateView, 
    FolderDeleteView
)

urlpatterns = [
    path('folder/<int:folder_id>/', views.folder_details, name='folder_details'),  # Folder details page
    path('add-to-folder/<int:book_id>/', views.add_book_to_folder, name='add_book_to_folder'),
    path('create-folder/', create_folder, name='create-folder'),
    path("folders/", FolderListView.as_view(), name="folder-list"),
    path("folders/new/", FolderCreateView.as_view(), name="folder-create"),
    path("folders/<int:pk>/edit/", FolderUpdateView.as_view(), name="folder-edit"),
    path("folders/<int:pk>/delete/", FolderDeleteView.as_view(), name="folder-delete"),
]
