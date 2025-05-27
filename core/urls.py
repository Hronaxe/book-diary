from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from user_books import views as user_books_views
from users import views as user_views
from . import views


urlpatterns = [
    path("", views.catalog, name="index"),
    #path("register", views.registration, name = "register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='custom_logout'),
    path('profile/', user_views.profile, name='profile'),
    path('catalog/', views.catalog, name='catalog'),
    path('info/', views.genres_and_authors, name='genres_and_authors'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('profile/books', user_books_views.user_books, name='user_books'),
    path('profile/add_author_popup', user_books_views.add_author_popup, name='add_author_popup'),
    path('profile/add_genre_popup', user_books_views.add_genre_popup, name='add_genre_popup'),
    path('profile/diary', views.diary, name='diary'),
    path('books/<int:pk>/set_status/', views.set_status, name='set_status'),
    path('profile/add_diary_entry/<int:pk>', views.add_diary_entry, name='add_diary_entry'),
    path('author',views.author,name='author'),
    path('genres',views.genres,name='genres'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('genres/<int:pk>/', views.genre_detail, name='genre_detail'),
    path('books/<int:book_id>/quotes/add/', views.add_quote, name='add_quote'),
    path('books/<int:book_id>/quotes/', views.book_quotes, name='book_quotes')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)