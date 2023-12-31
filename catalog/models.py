import django
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from user.models import User


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Products(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение', upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_of_last_change = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', null=True, blank=True)
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.title} {self.price}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            (
                'set_published',
                'Can publish posts'
            ),
        ]


class Contacts(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='Название компании')
    number = PhoneNumberField(verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email')
    office = models.CharField(max_length=150, verbose_name='Адрес офиса')

    def __str__(self):
        return f'{self.company_name}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'


class BlogEntry(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    public_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(verbose_name='Изображение')
    is_publish = models.BooleanField(verbose_name='Опубликовано', default=True)
    slug = models.CharField(max_length=150, verbose_name='slug', unique=True, null=True, blank=True)
    views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'запись блога'
        verbose_name_plural = 'записи блога'


class ProductVersion(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Версия продукта')
    version = models.IntegerField(verbose_name='Номер версии')
    version_name = models.CharField(max_length=150, verbose_name='Название версии')
    is_сurrent_version = models.BooleanField(verbose_name='Текущая версия')

    def __str__(self):
        return f'{self.version_name}'

    class Meta:
        verbose_name = 'версия продукта'
        verbose_name_plural = 'версии продукта'
