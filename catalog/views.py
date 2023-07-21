from django.shortcuts import render

from catalog.models import Products, Contacts


def home(request):
    print(list(Products.objects.all().order_by('date_of_create'))[-6:])
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(name, email, message)

    contact = Contacts.objects.get(pk=1)
    context = {
        'contact': contact
    }
    return render(request, 'catalog/contacts.html', context)
