from django import forms

from catalog.models import BlogEntry


class BlogEntryForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ('title', 'content', 'preview', 'is_publish',)
        widgets = {
            'title': forms.TextInput(
                attrs={'type': 'text', 'name': 'title', 'class': 'form-control'}),
            'content': forms.Textarea(
                attrs={'type': 'text', 'name': 'content', 'class': 'form-control'}),
            'preview': forms.FileInput(
                attrs={'type': 'file', 'name': 'preview', 'class': 'form-control'}),
            'is_publish': forms.CheckboxInput(
                attrs={'type': 'checkbox', 'name': 'preview', 'class': 'form-check-input'}),
        }
