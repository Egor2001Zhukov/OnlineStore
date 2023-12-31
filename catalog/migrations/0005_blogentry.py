# Generated by Django 4.2.3 on 2023-08-14 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_products_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название компании')),
                ('public_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('content', models.TextField(verbose_name='Содержимое')),
                ('preview', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('is_publish', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('slug', models.CharField(max_length=150, unique=True, verbose_name='slug')),
                ('views', models.IntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'запись блога',
                'verbose_name_plural': 'записи блога',
            },
        ),
    ]
