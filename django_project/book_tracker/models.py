from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self): # Change here
        return reverse('post-detail', kwargs={'pk': self.pk})
    
# Dummy
# book_tracker/models.py

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateField()

    def __str__(self):
        return self.title
