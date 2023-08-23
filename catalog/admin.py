from django.contrib import admin

from catalog.models import Products, Category, Contacts, BlogEntry, ProductVersion


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('title',)


@admin.register(Contacts)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'number', 'email', 'office')


@admin.register(BlogEntry)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'version_name', 'is_сurrent_version')
