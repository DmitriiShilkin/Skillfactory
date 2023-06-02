from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import BaseRegisterView, login_with_code_view, usual_login_view

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    # path('login/', usual_login_view, name='login'),
    path('login_with_code/', login_with_code_view, name='login_with_code'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
]
