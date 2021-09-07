# Generated by Django 3.2.6 on 2021-09-05 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teachers', '0013_auto_20210904_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teachers.location', verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='teachers.specialization', verbose_name='Специализация'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Учитель'),
        ),
    ]
