from django.shortcuts import render, redirect
import random
from string import hexdigits
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from django.conf import settings

from .forms import BaseRegisterForm
from .models import OneTimeCode


# Create your views here.
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'sign/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BaseRegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print("SIGNUP FORM IS VALID")
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        else:
            print("SIGNUP FORM IS INVALID")

        return redirect('activate', request.POST['username'])


class ActivateView(CreateView):
    template_name = 'sign/activate.html'

    def get_context_data(self, **kwargs):
        user_ = self.kwargs.get('user')
        if not OneTimeCode.objects.filter(user=user_).exists():
            code = ''.join(random.sample(hexdigits, 5))
            OneTimeCode.objects.create(user=user_, code=code)
            user = User.objects.get(username=user_)
            send_mail(
                subject='Код активации',
                message=f'Код ативации аккаунта: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = request.path.split('/')[-1]
            if OneTimeCode.objects.filter(code=request.POST['code'], user=user).exists():
                User.objects.filter(username=user).update(is_active=True)
                OneTimeCode.objects.filter(code=request.POST['code'], user=user).delete()
            else:
                return render(self.request, 'sign/invalid_code.html')
        return redirect('login')
