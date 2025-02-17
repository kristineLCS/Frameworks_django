from django.contrib import admin
import requests
from django import forms
from .models import Post, Book, Genre, Announcement
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

admin.site.register(Post)

class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data.get('title')

        # Use Google Books API to fetch details
        API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
        url = f"https://www.googleapis.com/books/v1/volumes?q={title}&key={API_KEY}"

        response = requests.get(url)
        data = response.json()

        # Debugging: Print the response from the API
        print("API Response:", data)

        # Check if a book was found
        if "items" in data:
            book_data = data["items"][0]["volumeInfo"]  # Get first book match

            # Debugging: Print what is being assigned
            print("Auto-filling data:")
            print("Author:", ", ".join(book_data.get("authors", [])))
            print("Published Date:", book_data.get("publishedDate", ""))
            print("Description:", book_data.get("description", ""))

            # Store values for later use in the save() method
            self.auto_fill_data = {
                'author': ", ".join(book_data.get("authors", [])),
                'published_date': book_data.get("publishedDate", ""),
                'description': book_data.get("description", ""),
                'google_books_id': book_data.get("id", "")
            }

        return title

    def save(self, commit=True):
        instance = super().save(commit=False)

        # If there is auto-filled data from the API
        if hasattr(self, 'auto_fill_data'):
            # Populate the fields with auto-filled data
            instance.author = self.auto_fill_data.get('author', '')
            instance.description = self.auto_fill_data.get('description', '')
            instance.google_books_id = self.auto_fill_data.get('google_books_id', '')

            # Handle published_date formatting
            published_date_str = self.auto_fill_data.get('published_date', "")
            if published_date_str:
                try:
                    # If the date is only a year (YYYY), append "-01-01" to make it YYYY-MM-DD
                    if len(published_date_str) == 4:
                        published_date_str += "-01-01"
                    # If the date is YYYY-MM, append "-01" to make it YYYY-MM-DD
                    elif len(published_date_str) == 7:
                        published_date_str += "-01"

                    instance.published_date = datetime.strptime(published_date_str, "%Y-%m-%d").date()
                except ValueError:
                    instance.published_date = None

        if commit:
            instance.save()

        return instance

# Register the new form in the admin panel
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'author', 'published_date')  # Show these in admin

admin.site.register(Book, BookAdmin)
admin.site.register(Announcement)


# admin.site.register(Genre)  # Register Genre model

