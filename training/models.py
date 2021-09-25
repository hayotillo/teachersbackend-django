from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from courses.models import *

User = get_user_model()


class Training(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=50, blank=False, verbose_name='Слуг')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    about = models.TextField(max_length=2000, blank=True, verbose_name='О нас')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainings', verbose_name='Пользователь')
    courses = GenericRelation(Course, related_name='training', verbose_name='Курсы')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'trainings_trainings'
        verbose_name = 'Учебный центр'
        verbose_name_plural = 'Учебные центры'


