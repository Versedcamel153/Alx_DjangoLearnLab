from bookshelf.models import Book

# Retrieve and update the book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Output the updated book
book.title