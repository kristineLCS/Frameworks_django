from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'
    
class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"

class BookFolder(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='book_folders')
    book = models.ForeignKey('book_tracker.Book', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} in {self.folder.name}"