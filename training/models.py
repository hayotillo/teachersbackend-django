from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Training(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=50, blank=False, verbose_name='Слуг')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    about = models.TextField(max_length=2000, blank=True, verbose_name='О нас')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainings', verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'trainings_trainings'
        verbose_name = 'Учебный центр'
        verbose_name_plural = 'Учебные центры'


class Course(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=255, blank=False, verbose_name='Слуг')
    price = models.CharField(max_length=10, blank=True, verbose_name='Цена')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Длительность')
    duration = models.CharField(max_length=10, blank=True, verbose_name='Длительность')
    about = models.TextField(max_length=10000, blank=True, verbose_name='О курсе')

    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Учебный центр'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'trainings_courses'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
