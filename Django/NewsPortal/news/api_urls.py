from django.urls import path, include
#импорт кэширования отдельных страниц
# from django.views.decorators.cache import cache_page
from rest_framework import routers

from .views import PostViewSet, CategoryViewSet, AuthorViewSet

router = routers.DefaultRouter()

router.register(r'news', PostViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'author', AuthorViewSet)


urlpatterns = [
# добавим кэширование на список всех публикаций. Раз в 1 минуту страничка будет записываться в кэш для экономии ресурсов.
#     path('', cache_page(60*1)(NewsList.as_view()), name='news_list'),
    path('', include(router.urls)),
# добавим кэширование на детальные публикации. Раз в 5 минут публикация будет записываться в кэш для экономии ресурсов.
#     path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail')
    path('api-auth/', include('rest_framework.urls'))
]
