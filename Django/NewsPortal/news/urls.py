from django.urls import path
from .views import (NewsList, PostDetail, PostSearch, NewsCreate, NewsEdit, NewsDelete,
                    make_author, CategoryList, subscribe)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('mkauthor/', make_author, name='make_author'),
    path('category/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe/', subscribe, name='subscribe_list'),
    path('create/error/', NewsCreate.as_view(template_name='news/news_create_error.html'), name='news_create_error'),
]
