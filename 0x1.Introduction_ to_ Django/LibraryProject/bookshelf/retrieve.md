from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Output book details
book.title, book.author, book.publication_year