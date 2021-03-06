# Generated by Django 3.2.6 on 2021-09-29 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_rename_name_grade_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время создание'),
        ),
        migrations.AlterField(
            model_name='book',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Время обновление'),
        ),
    ]
