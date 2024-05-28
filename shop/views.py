from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Cart, Order
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .forms import UserProfileForm, BookForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag, TaggedItem
import random

def home(request):
    books = Book.objects.all()[:10]
    tags = Tag.objects.annotate(num_books=Count('taggit_taggeditem_items')).order_by('-num_books')[:50]

    max_num_books = max(tag.num_books for tag in tags) if tags else 0
    min_size = 10
    max_size = 30
    for tag in tags:
        tag.size = min_size + (max_size - min_size) * (tag.num_books / max_num_books)

    return render(request, 'shop/home.html', {'books': books, 'tags': tags})

def book_list(request):
    tag_name = request.GET.get('tag')
    if tag_name:
        books = Book.objects.filter(tags__name=tag_name)
    else:
        books = Book.objects.all()
    tags = Tag.objects.annotate(num_books=Count('taggit_taggeditem_items')).order_by('-num_books')[:50]
    return render(request, 'shop/book_list.html', {'books': books, 'tags': tags})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'shop/book_detail.html', {'book': book})

@login_required
@require_POST
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.books.add(book)
    return JsonResponse({'message': 'カートに追加されました'})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total_price = sum(book.price for book in cart.books.all())
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'total_price': total_price})

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(user=request.user)
    order.books.set(cart.books.all())
    cart.books.clear()

    # 注文確認メールを送信
    subject = '注文確認'
    message = f'注文が確定しました。注文番号: {order.id}'
    recipient_list = [request.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    
    return redirect('shop:order_history')
    
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    order_summaries = []
    
    for order in orders:
        total_price = sum(book.price for book in order.books.all())
        order_summaries.append({
            'order': order,
            'total_price': total_price
        })

    return render(request, 'shop/order_history.html', {'order_summaries': order_summaries})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('shop:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'shop/profile.html', {'form': form})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.creator = request.user  # 現在のユーザーを作成者として設定
            book.save()
            form.save_m2m()  # Many-to-many関係を保存
            return redirect('shop:book_list')
    else:
        form = BookForm()
    return render(request, 'shop/add_book.html', {'form': form})

@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.creator != request.user:
        return HttpResponseForbidden("他のユーザーが追加した同人誌は編集できません。")
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('shop:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'shop/book_form.html', {'form': form, 'book': book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.creator != request.user:
        return HttpResponseForbidden("他のユーザーが追加した同人誌は削除できません。")
    
    if request.method == 'POST':
        book.delete()
        return redirect('shop:book_list')
    return render(request, 'shop/book_confirm_delete.html', {'book': book})

@login_required
@require_POST
def remove_from_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart.books.remove(book)
    return redirect('shop:cart_detail')