from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def registration(request):
    return render(request, 'register.html')

def custom_logout_view(request):
    logout(request)
    return redirect('/')

def profile(request):
    return render(request, 'base.html')

def user_books(request):
    return render(request, 'base.html')

def catalog(request):
    return render(request, 'base.html')

def genres_and_authors(request):
    return render(request, 'base.html')

def diary(request):
    return render(request, 'base.html')



