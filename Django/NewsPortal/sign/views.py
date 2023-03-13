# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'sign/signup.html'
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/index.html'
