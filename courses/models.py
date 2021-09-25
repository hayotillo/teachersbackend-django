from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Название')
    slug = models.SlugField(max_length=255, blank=False, verbose_name='Слаг')
    description = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='Начинается в')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Заканчивается в')
    price = models.CharField(max_length=10, blank=True, verbose_name='Цена')

    content_object = GenericForeignKey()
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'courses_courses'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


