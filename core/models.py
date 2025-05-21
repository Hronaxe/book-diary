from django.db import models

# Create your models here.

class Book(models.Model):
    COVER_UPLOAD_PATH = 'covers/'

    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.CharField(max_length=255, verbose_name='Автор')
    publisher = models.CharField(max_length=255, verbose_name='Издательство')
    year = models.PositiveIntegerField(verbose_name='Год издания')
    page_count = models.PositiveIntegerField(verbose_name='Количество страниц')
    age_limit = models.CharField(max_length=10, verbose_name='Возрастное ограничение')
    genre = models.CharField(max_length=100, verbose_name='Жанр')
    annotation = models.TextField(verbose_name='Аннотация')

    cover = models.ImageField(upload_to=COVER_UPLOAD_PATH, verbose_name='Обложка')
