from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    COVER_UPLOAD_PATH = 'covers/'

    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    publisher = models.CharField(max_length=255, verbose_name='Издательство')
    year = models.PositiveIntegerField(verbose_name='Год издания')
    page_count = models.PositiveIntegerField(verbose_name='Количество страниц')
    age_limit = models.CharField(max_length=10, verbose_name='Возрастное ограничение')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    annotation = models.TextField(verbose_name='Аннотация')
    text_file = models.FileField(upload_to='texts/', blank=True, null=True)

    cover = models.ImageField(upload_to=COVER_UPLOAD_PATH, verbose_name='Обложка')
    def __str__(self):
        return self.title

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote by {self.user.name} for {self.book.title}"

class UserBookStatus(models.Model):
    STATUS_CHOICES = (
        ('reading', 'Читаю'),
        ('read', 'Прочитал'),
        ('planned', 'В планах'),
        ('dropped', 'Брошено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.name} - {self.book.title} - {self.status}"

class ReadingDiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    emotions_rating = models.PositiveSmallIntegerField(default=1)  # 1-5
    plot_originality = models.PositiveSmallIntegerField(default=1)  # 1-5
    character_development = models.PositiveSmallIntegerField(default=1)
    world_building = models.PositiveSmallIntegerField(default=1)
    romance = models.PositiveSmallIntegerField(default=1)
    humor = models.PositiveSmallIntegerField(default=1)
    meaning = models.PositiveSmallIntegerField(default=1)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diary entry by {self.user.name} for {self.book.title}"
