from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import BaseRegisterView, ActivateView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('activate/<str:user>', ActivateView.as_view(), name='activate'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
]
