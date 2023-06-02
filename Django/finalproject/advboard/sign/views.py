# from django.shortcuts import render
import random

from django.contrib.auth import authenticate, login
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BaseRegisterForm
from .models import OneTimeCode


# Функция случайных номеров
def random_str():
    _str = '1234567890abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(_str) for i in range(6))


def email_send(request):
    pass
    return render(request, 'email_send.html')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('login')


def usual_login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        OneTimeCode.objects.create(code=random_str(), user=user)
        # email_send()
        # перенаправить на нужную страницу
        redirect('/login_with_code/')
    else:
        # вернуть сообщение об ошибке "не верный логин"
        pass


def login_with_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    if OneTimeCode.objects.filter(code=code, user__username=username).exists():
        login(request, username)
    else:
        # сообщение об ошибке
        pass


# def login_with_code_view(request):
#     user = User.objects.get(pk=request.user.id)
#     code = random_str()
#     otc = OneTimeCode.objects.create(code=code, user=user)
#
#     text = '''You can enter to our secret page
#     http://example.com/secret/page?otcode=%s
#     without your login and password''' % code
#
#     user.email_user('login with one-time code', text)
#
#     return render(request, 'sign/login.html')
