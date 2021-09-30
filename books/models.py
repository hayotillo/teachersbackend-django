from django.db import models
from django.utils.html import format_html


class Grade(models.Model):
    number = models.PositiveSmallIntegerField(unique=True, blank=True, verbose_name='Класс')

    def __str__(self):
        return str(self.number)

    class Meta:
        db_table = 'books_grades'
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Subject(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=255, blank=False, verbose_name='Слаг')

    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books_subjects'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Publisher(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=255, blank=False, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books_publishers'
        verbose_name = 'Издание'
        verbose_name_plural = 'Издании'


class Author(models.Model):
    full_name = models.CharField(max_length=255, blank=False, verbose_name='Ф.И.О')
    slug = models.SlugField(max_length=255, blank=False, verbose_name='Слаг')

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'books_authors'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=255, blank=False, verbose_name='Слаг')
    image = models.ImageField(upload_to='uploads/books/images/%Y/%m/%d', blank=True, verbose_name='Картинка')
    file = models.FileField(upload_to='uploads/books/files/%Y/%m/%d', blank=True, verbose_name='Файл')
    url = models.CharField(max_length=255, blank=True, verbose_name='Ссылка на файл')
    statuses = (('published', 'Опубликовано'), ('unpublished', 'Не опубликовано'))
    status = models.CharField(max_length=20, blank=False, choices=statuses, verbose_name='Статус')
    year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Дата издание')
    formats = (('pdf', 'PDF'), ('djvu', 'DJVU'))
    format = models.CharField(max_length=10, blank=True, null=True, choices=formats, verbose_name='Формат')
    pages = models.PositiveIntegerField(blank=True, null=True, verbose_name='Страниц')
    quantities = (('ebook', 'eBook'), ('scan', 'Skaner'))
    quality = models.CharField(max_length=10, blank=True, null=True, choices=quantities, verbose_name='Качество')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Время создание')
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='Время обновление')

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, related_name='books')
    authors = models.ManyToManyField(Author, verbose_name='books', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'books_books'
        verbose_name = 'Книгу'
        verbose_name_plural = 'Книги'

    def image_tag(self):
        return format_html(f'<img src={self.image.url} />')

    image_tag.short_description = 'Картинка'
