from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from user_books.forms import AuthorForm
from .models import Book, Genre, Author, UserBookStatus


def home(request):
    return render(request, 'home.html')

def registration(request):
    return render(request, 'register.html')

def custom_logout_view(request):
    logout(request)
    return redirect('/')

def catalog(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    authors = Author.objects.all()

    q = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    author_id = request.GET.get('author', '')
    year = request.GET.get('year', '')

    if q:
        books = books.filter(title__icontains=q) | books.filter(author__name__icontains=q)

    if genre_id:
        books = books.filter(genre_id=genre_id)

    if author_id:
        books = books.filter(author_id=author_id)

    if year:
        books = books.filter(year=year)

    context = {
        'books': books,
        'genres': genres,
        'authors': authors,
    }
    return render(request, 'catalog.html', context)

def genres_and_authors(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    context = {
        'authors': authors,
        'genres': genres,
    }
    return render(request, 'genres_and_authors.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    status_choices = UserBookStatus.STATUS_CHOICES
    try:
        user_status = UserBookStatus.objects.get(user=request.user, book=book).status
    except UserBookStatus.DoesNotExist:
        user_status = None

    return render(request, 'book_detail.html', {'book': book, 'status_choices': status_choices, 'user_status': user_status})

def profile(request):
    return render(request, 'base.html')

def user_books(request):
    return render(request, 'base.html')


def genres_and_authors(request):
    return render(request, 'base.html')

def diary(request):
    return render(request, 'base.html')

def set_status(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        status = request.POST.get('status')
        obj, created = UserBookStatus.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={'status': status},
        )
    return redirect('book_detail', pk=pk)



