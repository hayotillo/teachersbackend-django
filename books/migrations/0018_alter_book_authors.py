# Generated by Django 3.2.6 on 2021-09-29 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_alter_book_authors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(blank=True, to='books.Author', verbose_name='books'),
        ),
    ]
