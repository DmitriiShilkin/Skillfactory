from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    headline = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'headline',
            'content',
            'category',
            'author',
        ]

    def clean(self):
        cleaned_data = super().clean()
        headline = cleaned_data.get("headline")
        content = cleaned_data.get("content")

        if headline == content:
            raise ValidationError(
                "Заголовок не должен быть идентичен содержанию!"
            )
        return cleaned_data


class PostDeleteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = []
