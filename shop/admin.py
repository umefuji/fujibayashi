from django.contrib import admin
from .models import Author, Book, Tag, Cart, Order

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(Order)
