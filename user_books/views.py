from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user_books.forms import BookForm, AuthorForm, GenreForm


# Create your views here.

@login_required # Require user logged in before they can access profile page
def user_books(request):
    return render(request, 'user_books/user_books.html')

@login_required
def user_books(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        form.instance.uploaded_by = request.user
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            book.save()
            return redirect('user_books')
    else:
        form = BookForm()
    return render(request, 'user_books/user_books.html', {'form': form})

def add_author_popup(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return HttpResponse(
                f"<script>window.opener.dismissAddAnotherPopup(window, '{author.pk}', '{author}', 'author');</script>"
            )
    else:
        form = AuthorForm()
    return render(request, 'user_books/add_author_popup.html', {'form': form})

def add_genre_popup(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save()
            return HttpResponse(
                f"<script>window.opener.dismissAddAnotherPopup(window, '{genre.pk}', '{genre}', 'genre');</script>"
            )
    else:
        form = GenreForm()
    return render(request, 'user_books/add_genre_popup.html', {'form': form})


