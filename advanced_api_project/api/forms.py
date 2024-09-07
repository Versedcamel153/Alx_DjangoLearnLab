from django import forms
from .models import Book
from datetime import date

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def validate_publication_year(self):
        publication_year = self.cleaned_data.get('publication_year')
        if publication_year > date.today().year:
            raise forms.ValidationError("Publication year 2 should not be in the future!")
        return publication_year