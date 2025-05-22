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
            return redirect('home') # Redirect user to Homepage
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import login, authenticate
# from .forms import UserRegisterForm

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save user to DB
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')  # Get raw password

#             # Authenticate and login the user
#             user = authenticate(username=username, password=raw_password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'Welcome, {username}!')
#                 return redirect('home')
#             else:
#                 messages.warning(request, 'Authentication failed. Please log in manually.')
#                 return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'register.html', {'form': form})
