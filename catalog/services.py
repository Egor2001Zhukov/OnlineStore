from catalog.models import Category


def get_categories(title: str):

    Category.objects.get(title)
    return Category.objects.all()
