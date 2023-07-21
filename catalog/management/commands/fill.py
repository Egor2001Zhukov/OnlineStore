import json
import subprocess

from django.core.management import BaseCommand, call_command

from catalog.models import Products, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        # with open('catalog_products_data.json', encoding='utf-8') as file:
        #     data = json.load(file)
        #     products_for_create = []
        #     for item in data:
        #         category = Category.objects.get(id=item['fields']['category'])
        #         item['fields']['category'] = category
        #         products_for_create.append(Products(**item['fields']))
        # Products.objects.bulk_create(products_for_create)
        call_command('flush', '--noinput')
        call_command('loaddata', 'catalog_data.json')

