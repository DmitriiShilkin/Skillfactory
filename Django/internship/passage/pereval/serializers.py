from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Passage, Areas, User, Level, Coords, Images


# сериализатор вложенной модели регионов (горных систем), к которым относится перевал
class AreasSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(queryset=Areas.objects.all(), label='Принадлежность')

    class Meta:
        model = Areas
        fields = [
            'title',
        ]


# сериализатор вложенной модели уровней сложности перевала
class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring',
        ]


# сериализатор вложенной модели географичеких координат перевала
class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height',
        ]


# сериализатор вложенной модели пользователя, создающего запись о перевале
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'fam',
            'name',
            'otc',
            'phone',
            'email',
        ]

    def save(self, **kwargs):
        self.is_valid()
        user = User.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = User.objects.create(
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
                phone=self.validated_data.get('phone'),
                email=self.validated_data.get('email'),
            )
            return new_user


# сериализатор модели фотографий, прикрепляемых к перевалу
class ImagesSerializer(serializers.ModelSerializer):
    img = serializers.URLField(label='URL')

    class Meta:
        model = Images
        fields = [
            'title',
            'img',
        ]


# сериализатор модели самого перевала
class PassageSerializer(WritableNestedModelSerializer):
    area = AreasSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    user = UserSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Passage
        depth = 1
        fields = [
            'id',
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'area',
            'coords',
            'level',
            'spr_activities_types',
            'status',
            'images',
            'user',
         ]

    # переопределяем метод post
    def create(self, validated_data, **kwargs):
        area = validated_data.pop('area')
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user_ = User.objects.filter(email=user['email'])
        if user_.exists():
            user_serializer = UserSerializer(data=user)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        else:
            user = User.objects.create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        area = Areas.objects.create(**area)
        passage = Passage.objects.create(**validated_data, user=user, coords=coords, level=level, area=area)

        for image in images:
            img = image.pop('img')
            title = image.pop('title')
            Images.objects.create(img=img, passage=passage, title=title)

        return passage

