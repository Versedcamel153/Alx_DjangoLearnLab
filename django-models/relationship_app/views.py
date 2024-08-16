from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from .models import Book, Library
from .forms import BookForm

# Create your views here.
def book_list(request):
    books = Book.objects.all()

    return render(request, 'relationship_app/list_books.html', {'books':books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()
        return context

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect or return an HttpResponse after saving
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return "Invalid credentials"
        else:
            return "Invalid credentials"
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')


@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})