from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("todo...")

def registration(request):
    return render(request, 'register.html')

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



