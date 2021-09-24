from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from teachersbackend import helpers
User = get_user_model()


class UserAccount(models.Model):
    first_name = models.CharField(_('First name'), max_length=30, blank=False)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)
    photo = models.ImageField(_('User photo'), upload_to='uploads/users/photos/Y%/m%/d%/', blank=True)

    user = models.ForeignKey(
        User,
        related_name='user',
        on_delete=models.CASCADE,
        verbose_name='Аккаунт',
        blank=False
    )

    def save(self, *args, **kwargs):
        instance = super(UserAccount, self).save(*args, **kwargs)
        if self.photo:
            helpers.image_compress(self.photo)
        return instance

    def photo_tag(self):
        return format_html(f'<img src={self.photo.url} />')

    photo_tag.short_description = 'Фото'
    photo_tag.allow_tags = True

    def username_tag(self):
        return self.user.username

    username_tag.short_description = 'Логин'
    username_tag.allow_tags = True

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'users_users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
