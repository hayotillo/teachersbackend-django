from decimal import Decimal
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Sum
from django.utils.html import format_html
# from django.contrib.auth.models import User, AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
User = get_user_model()


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


class VoteManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def get_stars(self):
        like_count = self.likes().count()
        count = self.get_queryset().count()
        if like_count > 0:
            percent = like_count / (count / 100)
        else:
            percent = 0

        # if percent > 0:
        star1 = percent >= 1
        star2 = percent >= 40
        star3 = percent >= 60
        star4 = percent >= 80
        star5 = percent == 100
        stars = [star1, star2, star3, star4, star5]
        return stars


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


class Teacher(models.Model):
    first_name = models.CharField(max_length=30, blank=False, null=False, verbose_name='Имя')
    last_name = models.CharField(max_length=30, blank=True, null=False, verbose_name='Отчество')
    sur_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Фамилия')
    slug = models.CharField(max_length=255, blank=False, null=True, verbose_name='Слаг')
    statuses = (('active', 'Активный'), ('disable', 'Отключен'))
    status = models.CharField(max_length=10, blank=False, choices=statuses, verbose_name='Статус')
    about = RichTextField(blank=True, null=False, verbose_name='О себе')
    phone = models.CharField(max_length=20, blank=False, verbose_name='Телефон')
    phone2 = models.CharField(max_length=20, blank=True, verbose_name='Запасной телефон')
    post = models.CharField(max_length=100, blank=True, verbose_name='Дольжность')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Телеграм')
    youtube = models.CharField(max_length=100, blank=True, verbose_name='Ютуб')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    genders = (('male', 'Мурской'), ('female', 'Женский'))
    gender = models.CharField(max_length=6, choices=genders, blank=False, null=True, verbose_name='Пол')
    photo = models.ImageField(upload_to='uploads/photos/%Y/%m/%d/', blank=True, verbose_name='Фото')

    user = models.ForeignKey(User, blank=False, null=False, related_name='teacher', on_delete=models.CASCADE, verbose_name='Учитель')
    location = models.ForeignKey(Location, null=True, on_delete=models.DO_NOTHING, verbose_name='Адрес')
    specialization = models.ForeignKey(Specialization, null=True, on_delete=models.DO_NOTHING, verbose_name='Специализация')
    vote = GenericRelation('Vote', related_query_name='teachers')

    def save(self, *args, **kwargs):
        instance = super(Teacher, self).save(*args, **kwargs)
        if self.photo:
            image_path = f'{settings.MEDIA_ROOT}/{self.photo}'
            image = Image.open(image_path)
            image = image.resize((326, 326))
            image.save(image_path, quality=100, optimize=True)
        return instance

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def photo_tag(self):
        return format_html('<img src="%s" />' % self.photo.url)

    def username_tag(self):
        return self.user.username

    photo_tag.short_description = 'Фото'
    username_tag.short_description = 'Логин'
    photo_tag.allow_tags = True

    class Meta:
        db_table = 'teachers_teachers'
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Portfolio(models.Model):
    title = models.CharField(max_length=255, blank=False, verbose_name='Названия')
    image = models.ImageField(upload_to='uploads/portfolios/image/%Y/%m/%d/', blank=False, verbose_name='Фото')
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссыка')
    file = models.FileField(upload_to='uploads/portfolios/file/%Y/%m/%d/', blank=True, null=True, verbose_name='Файл')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='portfolios', verbose_name='Учитель')

    def __str__(self):
        return self.title

    def image_tag(self):
        return format_html(f'<img src="{self.image}" />')

    class Meta:
        db_table = 'teachers_portfolios'
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолии'


class Workplace(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Название учебного заведение')
    post = models.CharField(max_length=100, blank=True, verbose_name='Должность')
    start_date = models.DateField(blank=False, verbose_name='Дата устройсва')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата увальнения')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='workplaces', verbose_name='Учитель')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teachers_workplace'
        verbose_name = 'Место работы'
        verbose_name_plural = 'Место работы'


class Comment(models.Model):
    text = models.TextField(blank=False, verbose_name='Текст комментарии')
    reply = models.BigIntegerField(blank=True, null=True, verbose_name='Ответ на')
    statuses = (('published', 'Опубликован'), ('moderation', 'На модерации'))
    status = models.CharField(max_length=10, choices=statuses, blank=False, default='moderation', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновление')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Комментарии')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='comments', verbose_name='Учитель')

    def __str__(self):
        return self.text[: 20]

    class Meta:
        db_table = 'teachers_comments'
        verbose_name = 'Комментария'
        verbose_name_plural = 'Комментарии'



