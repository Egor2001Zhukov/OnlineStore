from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeView, ContactsView, ProductView, BlogEntryCreateView, BlogEntryDetailView, \
    BlogEntryListView, BlogEntryDeleteView, BlogEntryUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/<int:pk>', ProductView.as_view(), name='product'),
    path('blog/create', BlogEntryCreateView.as_view(), name='create_blog_entry'),
    path('blog/view/<slug:slug>', BlogEntryDetailView.as_view(), name='view_blog_entry'),
    path('blog/update/<slug:slug>', BlogEntryUpdateView.as_view(), name='update_blog_entry'),
    path('blog/delete/<slug:slug>', BlogEntryDeleteView.as_view(), name='delete_blog_entry'),
    path('blog/', BlogEntryListView.as_view(), name='blog'),
]
