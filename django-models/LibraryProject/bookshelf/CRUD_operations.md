# Create Operation

```python
from bookshelf.models import Book

# Create a book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Output the created book
book

# Retrieve and update the book title
book = Book.objects.get(title="1984")

book.title, book.author, book.publication_date

# Retrieve and update the book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Output the updated book
book.title

# delete book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

book


