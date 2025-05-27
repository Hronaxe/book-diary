from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # Save user to Database
            username = form.cleaned_data.get('username') # Get the username that is submitted
            messages.success(request, f'Account created for {username}!') # Show sucess message when account is created
            return redirect('login') # Redirect user to login
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required # Require user logged in before they can access profile page
def profile(request):
    return render(request, 'users/profile.html')
