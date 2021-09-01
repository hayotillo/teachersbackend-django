from django.db import models
from django.db.models import Sum
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Region(models.Model):
    name = models.CharField(max_length=30, blank=False, verbose_name='Регион')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teachers_regions'
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class District(models.Model):
    name = models.CharField(max_length=30, blank=False, verbose_name='Район')
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, verbose_name='Регион')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teachers_districts'
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Location(models.Model):
    name = models.CharField(max_length=30, blank=False, verbose_name='Адрес')
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING, verbose_name='Район')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teachers_locations'
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Specialization(models.Model):
    name = models.CharField(max_length=30, blank=False, verbose_name='Цпециальность')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teachers_specializations'
        verbose_name = 'Специализация'
        verbose_name_plural = 'Спациализации'


class Teacher(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, null=False, verbose_name='Отчество')
    sur_name = models.CharField(max_length=30, blank=True, null=False, verbose_name='Фамилия')
    statuses = (('active', 'Активный'), ('disable', 'Отключен'))
    status = models.CharField(max_length=10, blank=False, choices=statuses, verbose_name='Статус')
    about = models.TextField(blank=True, null=False, verbose_name='О себе')
    phone = models.CharField(max_length=20, blank=False, verbose_name='Телефон')
    phone2 = models.CharField(max_length=20, blank=True, verbose_name='Запасной телефон')
    post = models.CharField(max_length=100, blank=True, verbose_name='Дольжность')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Телеграм')
    youtube = models.CharField(max_length=100, blank=True, verbose_name='Ютуб')
    email = models.CharField(max_length=100, blank=True, verbose_name='Почта')
    photo = models.ImageField(upload_to='uploads/photos/%Y/%m/%d/', blank=True, verbose_name='Фото')

    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, verbose_name='Адрес')
    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING, verbose_name='Специализация')
    vote = GenericRelation('Vote', related_query_name='teachers')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def photo_tag(self):
        return format_html('<img src="%s" />' % self.photo.url)
    photo_tag.short_description = 'Фото'
    photo_tag.allow_tags = True

    class Meta:
        db_table = 'teachers_teachers'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Portfolio(models.Model):
    title = models.CharField(max_length=255, blank=False, verbose_name='Названия')
    image = models.ImageField(upload_to='uploads/portfolios/image/%Y/%m/%d/', blank=False, verbose_name='Фото')
    link = models.CharField(max_length=255, blank=True, verbose_name='Ссыка')
    file = models.FileField(upload_to='uploads/portfolios/file/%Y/%m/%d/', blank=True, verbose_name='Файл')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'teachers_portfolios'
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолии'


class Workplace(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Название учебного заведение')
    post = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    start_date = models.DateField(blank=False, verbose_name='Дата устройсва')
    end_date = models.DateField(blank=True, verbose_name='Дата увальнения')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teachers_workplace'
        verbose_name = 'Место работы'
        verbose_name_plural = 'Место работы'


class Comment(models.Model):
    text = models.TextField(blank=False, verbose_name='Текст комментарии')
    reply = models.IntegerField(blank=True, null=True, verbose_name='Ответ на')
    status = models.CharField(max_length=10, blank=False, default='moderation', verbose_name='Статус')
    created_at = models.DateTimeField(auto_created=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновление')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель')

    def __str__(self):
        return self.name[: 20]

    class Meta:
        db_table = 'teachers_comments'
        verbose_name = 'Комментария'
        verbose_name_plural = 'Комментарии'


class VoteManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class Vote(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTES = ((LIKE, 'Нравится'), (DISLIKE, 'Не нравится'))
    vote = models.SmallIntegerField(blank=True, choices=VOTES, verbose_name='Рейтинг')

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    objects = VoteManager()

    class Meta:
        db_table = 'teachers_votes'
