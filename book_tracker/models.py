from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): # Change here
        return reverse('post-detail', kwargs={'pk': self.pk})


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    google_books_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.google_books_id == "":
            self.google_books_id = None  # Convert empty strings to NULL
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


