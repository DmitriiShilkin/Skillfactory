from django.urls import path
from .views import (ArticleCreate, ArticleEdit, ArticleDelete)

urlpatterns = [
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
