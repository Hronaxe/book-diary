from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book, Genre, Author


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
        books = books.filter(publication_year=year)

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
    return render(request, 'book_detail.html', {'book': book})

def profile(request):
    return render(request, 'base.html')

def user_books(request):
    return render(request, 'base.html')


def genres_and_authors(request):
    return render(request, 'base.html')

def diary(request):
    return render(request, 'base.html')



