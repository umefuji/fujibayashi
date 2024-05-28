from django import forms
from django.contrib.auth.models import User
from .models import Book

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price', 'preview', 'sample_code_url', 'category', 'tags', 'digital_version', 'printed_version_available']
        widgets = {
            'price': forms.NumberInput(attrs={'step': 100})  
        }