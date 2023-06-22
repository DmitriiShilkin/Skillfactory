from django.urls import path, include

from rest_framework import routers

from .views import PostViewSet

router = routers.DefaultRouter()

router.register(r'news', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
