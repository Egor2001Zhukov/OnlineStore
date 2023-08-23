# Generated by Django 4.2.3 on 2023-08-21 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_products_date_of_create_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(verbose_name='Номер версии')),
                ('version_name', models.CharField(max_length=150, verbose_name='Название версии')),
                ('is_сurrent_version', models.BooleanField(verbose_name='Текущая версия')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products', verbose_name='Версия продукта')),
            ],
            options={
                'verbose_name': 'версия продукта',
                'verbose_name_plural': 'версии продукта',
            },
        ),
    ]
