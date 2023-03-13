from django.urls import path
from .views import (NewsList, PostDetail, PostSearch, NewsCreate, NewsEdit, NewsDelete, make_author)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('mkauthor/', make_author, name = 'make_author'),
]
