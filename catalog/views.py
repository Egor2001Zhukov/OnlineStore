from django.shortcuts import render

from catalog.models import Products, Contacts


def home(request):
    products = Products.objects.all()
    context = {
        'products': products,
        'contacts_active': 'text-white',
        'home_active': 'active',
        'category_active': 'text-white',
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(name, email, message)

    contact = Contacts.objects.get(pk=1)
    context = {
        'contact': contact,
        'contacts_active': 'active',
        'home_active': 'text-white',
        'category_active': 'text-white',
    }
    return render(request, 'catalog/contacts.html', context)


def product(request, product_id):
    product = Products.objects.get(pk=product_id)
    context = {
        'product': product,
        'contacts_active': 'text-white',
        'home_active': 'text-white',
        'category_active': 'active',
    }
    return render(request, 'catalog/product.html', context)
