from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ContactsView, ProductsDetailView, BlogEntryCreateView, BlogEntryDetailView, \
    BlogEntryListView, BlogEntryDeleteView, BlogEntryUpdateView, ProductsListView, ProductsUpdateView, \
    ProductsCreateView, ProductsDeleteView, CategoriesListView, CategoryDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('products/create', ProductsCreateView.as_view(), name='create_product'),
    path('products/view/<int:pk>', cache_page(60)(ProductsDetailView.as_view()), name='view_product'),
    path('products/update/<int:pk>', ProductsUpdateView.as_view(), name='update_product'),
    path('products/delete/<int:pk>', ProductsDeleteView.as_view(), name='delete_product'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('blog/create', BlogEntryCreateView.as_view(), name='create_blog_entry'),
    path('blog/view/<slug:slug>', BlogEntryDetailView.as_view(), name='view_blog_entry'),
    path('blog/update/<slug:slug>', BlogEntryUpdateView.as_view(), name='update_blog_entry'),
    path('blog/delete/<slug:slug>', BlogEntryDeleteView.as_view(), name='delete_blog_entry'),
    path('blog/', BlogEntryListView.as_view(), name='blog'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/view/<int:pk>', CategoryDetailView.as_view(), name='view_category'),
]
