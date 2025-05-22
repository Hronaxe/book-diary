from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.registration, name = "register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile')
]