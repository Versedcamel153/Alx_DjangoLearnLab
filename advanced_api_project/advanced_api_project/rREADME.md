# Book API

This project provides an API for managing a collection of books. The API allows users to view, create, update, and delete books. It leverages Django REST Framework (DRF) for handling API endpoints and permissions.

## Views Configuration

### BookListCreateAPIView

- **Description**: This view handles the retrieval of a list of books and the creation of a new book.
- **Methods**:
  - `GET`: Allows any user (authenticated or not) to view the list of books.
  - `POST`: Only authenticated users can create a new book.
- **Permissions**:
  - `GET`: `AllowAny`
  - `POST`: `IsAuthenticated`
- **URL**: `/api/books/`

### BookRetrieveUpdateDestroyAPIView

- **Description**: This view handles retrieving, updating, and deleting a book by its ID.
- **Methods**:
  - `GET`: Allows any user (authenticated or not) to view book details.
  - `PUT`, `PATCH`, `DELETE`: Only authenticated users can modify or delete the book.
- **Permissions**:
  - `GET`: `AllowAny`
  - `PUT`, `PATCH`, `DELETE`: `IsAuthenticated`
- **URL**: `/api/books/<int:pk>/`

## Custom Settings and Hooks

### Permissions

- **Custom Permission Class**: `IsAdminOrReadOnly`
  - **Description**: This permission class allows read access to any user but restricts write access to admin users only.
  - **Location**: `permissions.py`
  - **Usage**: Applied to views that need this specific access control.

### Form Validation

- **Custom Form**: `BookForm`
  - **Description**: A custom form for the `Book` model to handle additional validations.
  - **Location**: `forms.py`
  - **Usage**: Used in the CreateView and UpdateView for validating ISBN and other fields.

## Installation and Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

# Book API

...

## Filtering

### BookListCreateAPIView

- **Description**: This view handles the retrieval of a list of books and the creation of a new book.
- **Methods**:
  - `GET`: Allows any user (authenticated or not) to view the list of books.
  - `POST`: Only authenticated users can create a new book.
- **Filtering**:
  - **Attributes**:
    - `title`: Filter by book title (case-insensitive partial match).
    - `author`: Filter by book author (case-insensitive partial match).
    - `publication_year`: Filter by the publication year of the book.
  - **Example**:
    - `/api/books/?title=python`
    - `/api/books/?author=doe`
    - `/api/books/?publication_year=2021`
- **Permissions**:
  - `GET`: `AllowAny`
  - `POST`: `IsAuthenticated`
- **URL**: `/api/books/`

...