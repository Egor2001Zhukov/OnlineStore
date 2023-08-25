from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet

from catalog.models import BlogEntry, Products, ProductVersion


def forbidden_words_detect(text):
    forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
    for forbidden_word in forbidden_words:
        if forbidden_word in text:
            raise forms.ValidationError(f'Недопустимое слово \'{forbidden_word}\'')


class BlogEntryForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ('title', 'content', 'preview', 'is_publish',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        cleaned_data = self.cleaned_data.get('title')
        forbidden_words_detect(cleaned_data)
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        forbidden_words_detect(cleaned_data)
        return cleaned_data


class ProductVersionForm(forms.ModelForm):
    class Meta:
        model = ProductVersion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
