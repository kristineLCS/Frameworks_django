from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from .models import Post
from .models import Book
from .forms import BookSearchForm
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()



def home(request):
    context = {
       'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def posts(request):
    posts = Post.objects.all()  # Fetch all posts
    return render(request, 'blog/post_list.html', {'posts': posts})  # Update templat

@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5 # Pagination: django will only fetch 5 posts related to users request in the first page, the rest will automatically go to the next page.

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
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # New class PostDeleteView created here
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = "/" # Here we are redirecting the user back to the homepage after deleting a Post successfully


    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

# Search Bar
def book_search(request):
    form = BookSearchForm(request.GET)  # Get search query from request
    books = []

    if form.is_valid():
        query = form.cleaned_data['query']
        
        # Search for books in the database by title or author
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(authors__icontains=query)

    return render(request, 'blog/home.html', {'form': form, 'books': books})