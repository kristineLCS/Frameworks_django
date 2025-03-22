from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .models import Post, Book, Announcement
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
# from users.forms import BookSearchForm
from django.db.models import Q
from users.models import Folder
from .forms import AnnouncementForm


User = get_user_model()



def home(request):
    context = {
       'posts': Post.objects.all(),
       'announcements': Announcement.objects.order_by('-created_at')[:5]  # Fetch latest 5 announcements
    }
    return render(request, 'blog/home.html', context)


def posts(request):
    posts = Post.objects.all()  # Fetch all posts
    return render(request, 'blog/post_list.html', {'posts': posts})


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
    

class BaseCRUDView(SingleObjectMixin):
    """
    A universal CRUD base class to handle operations for any model.
    """
    model = None  # "None" - To be defined in child classes
    form_class = None 
    template_name = None
    success_url = None

    def get_queryset(self):
        if not self.request.user.is_staff:  # Only admins can manage announcements
            raise PermissionDenied("You do not have permission to access this content.")
        return self.model.objects.all()  # Admins can view all announcements

    def get_object(self, queryset=None):
        obj = self.model.objects.get(pk=self.kwargs["pk"])  # Get object manually
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to modify this item.")
        return obj



# Search Bar
def search_results(request):
    query = request.GET.get('q', '').strip()
    print(f"Search query: {query}")  # Debugging

    books = Book.objects.all()

    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)) if query else Book.objects.none()

    # Only fetch folders if the user is authenticated
    folders = Folder.objects.filter(user=request.user) if request.user.is_authenticated else []

    print("Search results view is being called!")
    print(f"User: {request.user} | Folders: {list(folders)}")  # Ensures folders are being retrieved

    return render(request, 'blog/search_results.html', {
        'books': books, 
        'folders': folders,
        'query': query,
})




# ANNOUNCEMENT BOARD
# Function to check if the user is an admin
def is_admin(user):
    return user.is_staff  # Allows only staff users (admins)

@login_required
@user_passes_test(is_admin)
def post_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user  # Assign current admin as author
            announcement.save()
            return redirect('blog-home')  # Redirect to homepage after posting
    else:
        form = AnnouncementForm()
    
    return render(request, 'blog/post_announcement.html', {'form': form})


class AnnouncementCreateView(BaseCRUDView, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "blog/post_announcement.html"
    success_url = reverse_lazy("blog-home")

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author as the logged-in admin
        return super().form_valid(form)
    
class AnnouncementUpdateView(BaseCRUDView, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "blog/post_announcement.html"
    success_url = reverse_lazy("blog-home")

from django.views.generic import DeleteView

class AnnouncementDeleteView(UserPassesTestMixin, DeleteView):
    model = Announcement
    template_name = "blog/confirm_announcement_delete.html"
    success_url = reverse_lazy("blog-home")

    def test_func(self):
        """Allow only admins to delete announcements"""
        return self.request.user.is_staff

    def get_template_names(self):
        print(f"Using template: {self.template_name}")  # Debugging
        return [self.template_name]

