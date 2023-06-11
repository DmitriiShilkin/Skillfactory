from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Passage, Coords, Level, Images, User
from .serializers import (PassageSerializer, LevelSerializer, CoordsSerializer, ImagesSerializer,
                          UserSerializer)


# Create your views here.
# представление для уровней сложности перевала
class LevelViewSet(viewsets.ModelViewSet):
    serializer_class = LevelSerializer
    queryset = Level.objects.all()


# # представление для регионов перевалов
# class AriasViewSet(viewsets.ModelViewSet):
#     serializer_class = AreasSerializer
#     queryset = Areas.objects.all()


# представление для географических координат перевала
class CoordsViewSet(viewsets.ModelViewSet):
    serializer_class = CoordsSerializer
    queryset = Coords.objects.all()


# представление для фотографий перевала
class ImagesViewSet(viewsets.ModelViewSet):
    serializer_class = ImagesSerializer
    queryset = Images.objects.all()


# представление для пользователя, который отправляет данные о перевале
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


# представление для перевала
class PassageViewSet(viewsets.ModelViewSet):
    serializer_class = PassageSerializer
    queryset = Passage.objects.all()
    filterset_fields = ('user__email',)

    # переопределяем метод, чтобы получить требуемые сообщения по ТЗ
    def create(self, request, *args, **kwargs):
        serializer = PassageSerializer(data=request.data)
        print(request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Успех',
                    'id': serializer.data['id']
                }
            )
        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Bad request',
                    'id': None
                }
            )
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка при выполнении операции',
                    'id': None
                }
            )
