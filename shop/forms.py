from django import forms
from django.contrib.auth.models import User
from .models import Book
from allauth.account.forms import SignupForm
from .models import Author
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','description', 'price', 'preview', 'sample_code_url', 'category', 'tags', 'digital_version', 'printed_version_available']
        widgets = {
            'price': forms.NumberInput(attrs={'step': 100})  
        }
class CustomSignupForm(SignupForm):
    is_author = forms.BooleanField(required=False, label="同人誌を売りますか？")

    def save(self, request):
        user = super().save(request)
        if self.cleaned_data.get('is_author'):
            if not Author.objects.filter(user=user).exists():
                Author.objects.create(user=user)
        return user