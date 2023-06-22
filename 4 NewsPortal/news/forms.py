from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from allauth.account.forms import SignupForm

from .models import Post


class PostForm(forms.ModelForm):
    headline = forms.CharField(min_length=20, label='Заголовок')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':100}), min_length=100, label='Содержание')

    class Meta:
        model = Post
        fields = [
            'headline',
            'content',
            'category',
        ]

        labels = {
            'category': _('Категория'),
        }

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


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
