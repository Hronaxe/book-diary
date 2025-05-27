from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from user_books.forms import AuthorForm
from .forms import ReadingDiaryEntryForm, QuoteForm
from .models import Book, Genre, Author, UserBookStatus, Quote, ReadingDiaryEntry
import random
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
def home(request):
    return render(request, 'home.html')

# def registration(request):
#     return render(request, 'registration_form.html')


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
    
    # Получаем среднюю оценку и количество оценок
    average_rating = book.average_rating()
    ratings_count = book.ratings_count()
    
    # Преобразуем рейтинг в целое число для звездочек, если он существует
    rating_stars = int(round(average_rating)) if average_rating else 0
    
    # Получаем статус книги для текущего пользователя (если авторизован)
    user_status = None
    if request.user.is_authenticated:
        try:
            status_obj = UserBookStatus.objects.get(user=request.user, book=book)
            user_status = status_obj.status
        except UserBookStatus.DoesNotExist:
            user_status = None
    
    # Получаем похожие книги (по жанру или автору)
    similar_books = Book.objects.filter(
        genre=book.genre
    ).exclude(pk=book.pk)[:6]  # Исключаем текущую книгу и берем 6 похожих
    
    # Варианты статусов для формы
    status_choices = UserBookStatus.STATUS_CHOICES
    
    context = {
        'book': book,
        'average_rating': average_rating,
        'rating_stars': rating_stars,
        'ratings_count': ratings_count,
        'user_status': user_status,
        'status_choices': status_choices,
        'similar_books': similar_books,
    }
    
    return render(request, 'book_detail.html', context)

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

def add_diary_entry(request, pk):
    book = get_object_or_404(Book, pk=pk)
    existing_entry = ReadingDiaryEntry.objects.filter(user=request.user, book=book).first()

    if request.method == 'POST':
        form = ReadingDiaryEntryForm(request.POST, instance=existing_entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.book = book
            entry.save()

            # Mark the book as read
            UserBookStatus.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'status': 'read'},
            )

            messages.success(request, f'Оценка для книги "{book.title}" успешно сохранена!')
            return redirect('book_detail', pk=book.id)
    else:
        form = ReadingDiaryEntryForm(instance=existing_entry)

    return render(request, 'review_entry.html', {
        'form': form,
        'book': book,
        'existing_entry': existing_entry,
    })


def catalog(request):
    books_qs = Book.objects.all()
    genres = Genre.objects.all()
    authors = Author.objects.all()

    q = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    author_id = request.GET.get('author', '')
    year = request.GET.get('year', '')

    if q:
        books_qs = books_qs.filter(title__icontains=q) | books_qs.filter(author__name__icontains=q)
    if genre_id:
        books_qs = books_qs.filter(genre_id=genre_id)
    if author_id:
        books_qs = books_qs.filter(author_id=author_id)
    if year:
        books_qs = books_qs.filter(year=year)

    # Применяем стабильную сортировку
    books_qs = books_qs.order_by('title', 'id')

    # Отладка: выводим общее количество книг
    print(f"Общее количество книг после фильтрации: {books_qs.count()}")

    paginator = Paginator(books_qs, 9)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        # Если страница пустая, возвращаем последнюю доступную страницу или пустой ответ для AJAX
        page_obj = paginator.page(paginator.num_pages) if paginator.num_pages > 0 else []

    all_books = list(Book.objects.all())
    random_books = random.sample(all_books, min(len(all_books), 3)) if all_books else []

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print(f"AJAX запрос - страница: {page_number}")
        print(f"Количество книг на странице: {len(page_obj.object_list)}")
        print(f"ID книг на странице: {[book.id for book in page_obj.object_list]}")
        print(f"Есть следующая страница: {page_obj.has_next()}")

        html = render_to_string('partials/book_list.html', {'books': page_obj})
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'book_ids': [book.id for book in page_obj.object_list],
        })

    return render(request, 'catalog.html', {
        'books': page_obj,
        'genres': genres,
        'authors': authors,
        'random_books': random_books,
    })
@login_required
def add_quote(request, book_id):

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        form.instance.book_id = book_id
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('book_quotes', book_id)
    else:
        form = QuoteForm()
    return render(request, 'add_quotes.html', {'form': form})


def book_quotes(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    quotes = Quote.objects.filter(book=book, user = request.user).order_by('-created_at')

    return render(request, 'book_quotes.html', {
        'book': book,
        'quotes': quotes
    })