from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    preview = models.FileField(upload_to='previews/', blank=True, null=True)
    sample_code_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, default='その他')  # デフォルト値を設定
    tags = TaggableManager()
    digital_version = models.FileField(upload_to='digital_books/', blank=True, null=True)
    printed_version_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_books', default=1)

    def __str__(self):
        return self.title
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'