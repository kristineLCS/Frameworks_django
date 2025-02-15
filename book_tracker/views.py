from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import Post, Book
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
# from users.forms import BookSearchForm
from django.db.models import Q
from users.models import Folder
from users.forms import FolderForm


User = get_user_model()



def home(request):
    context = {
       'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def posts(request):
    posts = Post.objects.all()  # Fetch all posts
    return render(request, 'blog/post_list.html', {'posts': posts})  # Update template


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5 # Pagination: django will only fetch 5 posts related to users request in the first page, the rest will automatically go to the next page.

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date_posted')
        print("Ordered Queryset:", list(queryset.values_list('title', 'date_posted')))  # Debugging
        print("Ordered Queryset Count:", queryset.count())  # Check number of posts
        return queryset

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user.posts.order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' # line added as django had a hard time finding where the file is located

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  # Added for new Posts to have a title and content section.
    template_name = 'blog/post_form.html'


    #Overriding form_valid method
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author on the form
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self): # Function to make sure logged in user can only edit their posts and not another user's post
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = "/" # redirecting the user back to the homepage after deleting a Post successfully


    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class BaseCRUDView:
    """
    A universal CRUD base class to handle operations for any model.
    """
    model = None  # "None" - To be defined in child classes
    form_class = None 
    template_name = None
    success_url = None
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)  # Restrict access to user's objects

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to modify this item.")
        return obj


# Search Bar
@login_required
def search_results(request):
    query = request.GET.get('q', '')
    print(f"Search query: {query}")  # Debugging

    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)) if query else Book.objects.none()
    
    # Fetch folders for the logged-in user
    folders = Folder.objects.filter(user=request.user)
    print("Search results view is being called!")
    print(f"User: {request.user} | Folders: {list(folders)}")  # Ensures folders are being retrieved

    return render(request, 'blog/search_results.html', {'books': books, 'folders': folders})
