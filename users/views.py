from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Folder, BookFolder
from book_tracker.models import Book
from book_tracker.views import BaseCRUDView
from .forms import FolderForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, f'The account {user.username} was created successfully!')
            return redirect('profile')  # Redirect to profile after login
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    # Get the user's folders to display them on the profile page
    folders = Folder.objects.filter(user=request.user)

    # Handle the form submission for creating a new folder
    folder_form = FolderForm(request.POST or None)  # Form for creating folders

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated') #Changes here
            return redirect('profile')
        
         # Handle folder creation form submission separately
        if folder_form.is_valid():
            folder = folder_form.save(commit=False)
            folder.user = request.user  # Assign the folder to the logged-in user
            folder.save()
            messages.success(request, "Folder created successfully.")  # Success message for folder creation
            return redirect('profile')  # Redirect to show the folder
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        folder_form = FolderForm()  # Empty form for creating a folder


    # Context to pass into the template
    context = {
        'u_form': u_form,
        'folders': folders,  # User's folders
        'folder_form': folder_form  # Folder creation form
    }

    return render(request, 'users/profile.html', context)

# Profile Folders
@login_required
def create_folder(request):
    if request.method == "POST":
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user  # Assign the folder to the logged-in user
            folder.save()
            return redirect('profile')  # Redirect to the profile page or folder list
    else:
        form = FolderForm()

    return render(request, 'users/create_folders.html', {'form': form})

@login_required
def add_book_to_folder(request, book_id):
    if request.method == "POST":
        folder_id = request.POST.get("folder_id")
        if not folder_id:
            messages.error(request, "No folder selected!")
            return redirect("search_results")  # Or any page you prefer

        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
        book = get_object_or_404(Book, id=book_id)

        if not BookFolder.objects.filter(folder=folder, book=book).exists():
            BookFolder.objects.create(folder=folder, book=book)

        messages.success(request, f"Book added to {folder.name}!")
        return redirect("search_results")



@login_required
def folder_details(request, folder_id):
    # Fetch the folder by its ID
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    
    # Get all books saved in this folder
    books_in_folder = BookFolder.objects.filter(folder=folder).select_related('book')  # Get the books associated with the folder
    
    # Context to pass to the template
    context = {
        'folder': folder,
        'books_in_folder': books_in_folder
    }
    
    return render(request, 'users/folder_details.html', context)


# List all folders for the logged-in user
class FolderListView(LoginRequiredMixin, BaseCRUDView, ListView):
    model = Folder
    template_name = "users/folder_list.html"
    context_object_name = "folders"

# Create a new folder
class FolderCreateView(LoginRequiredMixin, BaseCRUDView, CreateView):
    model = Folder
    form_class = FolderForm
    template_name = "users/update_folder.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Update a folder name
class FolderUpdateView(LoginRequiredMixin, UserPassesTestMixin, BaseCRUDView, UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = "users/update_folder.html"
    success_url = reverse_lazy("profile")

    def test_func(self):
        folder = self.get_object()
        return self.request.user == folder.user

# Delete a folder
class FolderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Folder
    template_name = "users/folder_confirm_delete.html"
    success_url = reverse_lazy("profile")
    
    def test_func(self):
        folder = self.get_object()
        return self.request.user == folder.user
    
    def get_queryset(self):
        print("FolderDeleteView is being called!")  # Debugging
        return Folder.objects.filter(user=self.request.user)
    

@login_required
def remove_book_from_folder(request, folder_id, book_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    book = get_object_or_404(Book, id=book_id)

    if book in folder.books.all():
        folder.books.remove(book)
        messages.success(request, "Book removed from folder successfully.")
    else:
        messages.error(request, "Book not found in folder.")

    return redirect("folder-detail", folder_id=folder.id)
