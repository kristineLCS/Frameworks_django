import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('GOOGLE_BOOKS_API_KEY')

# Test the API
query = 'Harry Potter'  # Can change the query to search for other books
url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    books = response.json()
    print(books)  # This will print the book details returned from the API
else:
    print(f"Error: {response.status_code}")
