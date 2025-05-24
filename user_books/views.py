from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user_books.forms import BookForm


# Create your views here.

@login_required # Require user logged in before they can access profile page
def user_books(request):
    return render(request, 'user_books/user_books.html')

@login_required
def user_books(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.uploaded_by = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'user_books/user_books.html', {'form': form})
