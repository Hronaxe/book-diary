from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views
from . import views


urlpatterns = [
    path("", views.home, name="index"),
    path("register", views.registration, name = "register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('profile/', user_views.profile, name='profile')
]