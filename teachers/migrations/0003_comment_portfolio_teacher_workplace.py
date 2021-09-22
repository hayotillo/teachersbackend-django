# Generated by Django 3.2.6 on 2021-09-22 06:19

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teachers', '0002_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Отчество')),
                ('sur_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Фамилия')),
                ('slug', models.CharField(max_length=255, null=True, verbose_name='Слаг')),
                ('status', models.CharField(choices=[('active', 'Активный'), ('disable', 'Отключен')], max_length=10, verbose_name='Статус')),
                ('about', ckeditor.fields.RichTextField(blank=True, verbose_name='О себе')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('phone2', models.CharField(blank=True, max_length=20, verbose_name='Запасной телефон')),
                ('post', models.CharField(blank=True, max_length=100, verbose_name='Дольжность')),
                ('telegram', models.CharField(blank=True, max_length=100, verbose_name='Телеграм')),
                ('youtube', models.CharField(blank=True, max_length=100, verbose_name='Ютуб')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[('male', 'Мурской'), ('female', 'Женский')], max_length=6, null=True, verbose_name='Пол')),
                ('photo', models.ImageField(blank=True, upload_to='uploads/photos/%Y/%m/%d/', verbose_name='Фото')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teachers.location', verbose_name='Адрес')),
                ('specialization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teachers.specialization', verbose_name='Специализация')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL, verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'Учитель',
                'verbose_name_plural': 'Учителя',
                'db_table': 'teachers_teachers',
            },
        ),
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название учебного заведение')),
                ('post', models.CharField(blank=True, max_length=100, verbose_name='Должность')),
                ('start_date', models.DateField(verbose_name='Дата устройсва')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дата увальнения')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workplaces', to='teachers.teacher', verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'Место работы',
                'verbose_name_plural': 'Место работы',
                'db_table': 'teachers_workplace',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Названия')),
                ('image', models.ImageField(upload_to='uploads/portfolios/image/%Y/%m/%d/', verbose_name='Фото')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссыка')),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/portfolios/file/%Y/%m/%d/', verbose_name='Файл')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='teachers.teacher', verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'Портфолио',
                'verbose_name_plural': 'Портфолии',
                'db_table': 'teachers_portfolios',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментарии')),
                ('reply', models.BigIntegerField(blank=True, null=True, verbose_name='Ответ на')),
                ('status', models.CharField(choices=[('published', 'Опубликован'), ('moderation', 'На модерации')], default='moderation', max_length=10, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата обновление')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='teachers.teacher', verbose_name='Учитель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Комментарии')),
            ],
            options={
                'verbose_name': 'Комментария',
                'verbose_name_plural': 'Комментарии',
                'db_table': 'teachers_comments',
            },
        ),
    ]
