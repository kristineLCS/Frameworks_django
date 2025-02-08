from django.core.management.base import BaseCommand
import requests
from book_tracker.models import Book
from datetime import datetime
import os
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')

class Command(BaseCommand):
    help = "Update missing book details using Google Books API"

    def handle(self, *args, **kwargs):
        books = Book.objects.filter(description__isnull=True)  # Find books missing descriptions

        for book in books:
            query = book.title
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}"
            response = requests.get(url)
            data = response.json()

            if "items" in data:
                book_data = data["items"][0]["volumeInfo"]

                # Update missing details
                book.author = ", ".join(book_data.get("authors", [])) or book.author
                book.description = book_data.get("description", "") or book.description
                
                # Convert published date
                published_date_str = book_data.get("publishedDate", "")
                if published_date_str:
                    try:
                        book.published_date = datetime.strptime(published_date_str, "%Y-%m-%d").date()
                    except ValueError:
                        book.published_date = None
                
                # Ensure google_books_id is assigned
                book.google_books_id = book_data.get("id", None) or None
                
                book.save()
                print(f"Updated: {book.title}")

        print("Book update process completed.")
