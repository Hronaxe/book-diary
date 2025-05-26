from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from user_books.forms import AuthorForm
from .forms import ReadingDiaryEntryForm
from .models import Book, Genre, Author, UserBookStatus


def home(request):
    return render(request, 'home.html')

def registration(request):
    return render(request, 'register.html')


def author(req):
    authors = Author.objects.all()
    return render(req, 'author.html', {'authors': authors})

def genres(req):
    genres = Genre.objects.all()
    return render(req, 'genres.html', {'genres': genres})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    return render(request, 'catalog/author_detail.html', {
        'author': author,
        'books': books
    })

def genre_detail(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = Book.objects.filter(genre=genre)
    return render(request, 'catalog/genre_detail.html', {'genre': genre, 'books': books})

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


def genres_and_authors(request):
    return render(request, 'base.html')

def diary(request):
    status_filter = request.GET.get('status')

    qs = UserBookStatus.objects.filter(user=request.user)
    if status_filter in dict(UserBookStatus.STATUS_CHOICES):
        qs = qs.filter(status=status_filter)

    return render(request, 'diary.html', {
        'statuses': UserBookStatus.STATUS_CHOICES,
        'user_books': qs.select_related('book'),
        'current_filter': status_filter,
    })

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

@login_required
def add_diary_entry(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = ReadingDiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.book = book
            entry.save()

            obj, created = UserBookStatus.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'status': 'read'},
            )

            return redirect('book_detail', pk=book.id)
    else:
        form = ReadingDiaryEntryForm(initial={'book': book})

    return render(request, 'review_entry.html', {
        'form': form,
        'book': book,
    })


