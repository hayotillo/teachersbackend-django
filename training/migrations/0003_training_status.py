# Generated by Django 3.2.6 on 2021-09-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_delete_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='status',
            field=models.CharField(choices=[('active', 'Активный'), ('disable', 'Отключен')], default=1, max_length=10, verbose_name='Статус'),
            preserve_default=False,
        ),
    ]
