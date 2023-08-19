from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from pytils.translit import slugify

from catalog.forms import BlogEntryForm
from catalog.models import Products, Contacts, BlogEntry

import os
from dotenv import load_dotenv
load_dotenv()


class HomeView(ListView):
    model = Products
    template_name = 'catalog/home.html'


class ContactsView(View):

    def get(self, request):
        contact = Contacts.objects.get(pk=1)
        return render(request, 'catalog/contacts.html', context={'object': contact})

    def post(self, request):
        contact = Contacts.objects.get(pk=1)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(name, email, message)
        return render(request, 'catalog/contacts.html', context={'object': contact})


class ProductView(DetailView):
    model = Products
    template_name = 'catalog/product.html'


class BlogEntryCreateView(CreateView):
    form_class = BlogEntryForm
    template_name = 'catalog/blogentry_form.html'

    def form_valid(self, form):
        if form.is_valid():
            slug = slugify(form.cleaned_data.get('title') + '0')
            while BlogEntry.objects.filter(slug=slug).first():
                number_repeat = str(int(slug[-1]) + 1)
                slug = slugify(BlogEntry.objects.get(slug=slug).slug[:-1] + number_repeat)
            new_entry = form.save()
            new_entry.slug = slug
            new_entry.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view_blog_entry', kwargs={'slug': self.object.slug})


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    success_url = reverse_lazy('catalog:blog')


class BlogEntryUpdateView(UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        slug = slugify(form.cleaned_data.get('title') + '0')
        while BlogEntry.objects.filter(slug=slug).first():
            number_repeat = str(int(slug[-1]) + 1)
            slug = slugify(BlogEntry.objects.get(slug=slug).slug[:-1] + number_repeat)
        new_entry = form.save()
        new_entry.slug = slug
        new_entry.save()
        return super().form_valid(form)


class BlogEntryDetailView(DetailView):
    model = BlogEntry

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        if self.object.views == 100:
            subject = 'Поздравления'
            message = f'Ура, у поста {self.object.title} 100 просмотров!'
            from_email = os.getenv('EMAIL_HOST_USER')
            recipient_list = [os.getenv('RECIPIENT_LIST')]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return self.object


class BlogEntryListView(ListView):
    model = BlogEntry

    def get_queryset(self):
        return super().get_queryset().filter(is_publish=True)
