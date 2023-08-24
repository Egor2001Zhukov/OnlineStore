import os

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from dotenv import load_dotenv
from pytils.translit import slugify

from catalog.forms import BlogEntryForm, ProductsForm, ProductVersionForm
from catalog.models import Products, Contacts, BlogEntry, ProductVersion

load_dotenv()


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


class ProductsListView(ListView):
    model = Products
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return
        context = super().get_context_data(**kwargs)
        print(self.request.user.is_authenticated)
        for product in context['object_list']:
            active_version = ProductVersion.objects.filter(product=product, is_сurrent_version=True).first()
            product.active_version = active_version
        return context


class ProductsCreateView(CreateView):
    form_class = ProductsForm
    template_name = 'catalog/products_form.html'

    def get_success_url(self):
        return reverse('catalog:view_product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            new_product = form.save()
            new_product.user = self.request.user
            new_product.save()
        return super().form_valid(form)


class ProductsDetailView(DetailView):
    model = Products

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return
        return super().get_context_data(**kwargs)


class ProductsUpdateView(UpdateView):
    model = Products
    form_class = ProductsForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return
        context = super().get_context_data(**kwargs)
        # Формирование формсета
        VersionFormSet = inlineformset_factory(Products, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = VersionFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data().get('formset')
        if formset.is_valid():
            count_is_сurrent_version = 0
            for f in formset:
                if formset.can_delete and formset._should_delete_form(f):
                    continue
                if f.cleaned_data.get('is_сurrent_version'):
                    count_is_сurrent_version += 1
                    if count_is_сurrent_version > 1:
                        form.add_error(None, "Не может быть больше одной текущей версии")
                        return self.form_invalid(form=form)
            formset.save()
            return super().form_valid(form=form)


class ProductsDeleteView(DeleteView):
    model = Products
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return
        return super().get_context_data(**kwargs)


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
