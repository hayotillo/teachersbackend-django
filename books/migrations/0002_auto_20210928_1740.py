# Generated by Django 3.2.6 on 2021-09-28 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveIntegerField(blank=True, max_length=2, unique=True, verbose_name='')),
            ],
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Книгу', 'verbose_name_plural': 'Книги'},
        ),
        migrations.AddField(
            model_name='subject',
            name='grade',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='books.grade'),
            preserve_default=False,
        ),
    ]
