from django.urls import path
#импорт кэширования отдельных страниц
# from django.views.decorators.cache import cache_page

from .views import (NewsList, PostDetail, PostSearch, NewsCreate, NewsEdit, NewsDelete,
                    make_author, CategoryList, subscribe)

urlpatterns = [
# добавим кэширование на список всех публикаций. Раз в 1 минуту страничка будет записываться в кэш для экономии ресурсов.
#     path('', cache_page(60*1)(NewsList.as_view()), name='news_list'),
    path('', NewsList.as_view(), name='news_list'),
# добавим кэширование на детальные публикации. Раз в 5 минут публикация будет записываться в кэш для экономии ресурсов.
#     path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
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
