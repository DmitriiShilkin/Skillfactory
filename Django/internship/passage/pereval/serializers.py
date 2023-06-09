from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Passage, Areas, User, Level, Coords, Images


class AreasSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(queryset=Areas.objects.all(), label='Принадлежность')

    class Meta:
        model = Areas
        fields = [
            'title',
        ]


class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring',
        ]


class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height',
        ]


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


class ImagesSerializer(serializers.ModelSerializer):
    img = serializers.URLField()

    class Meta:
        model = Images
        fields = [
            'title',
            'img',
        ]


class PassageSerializer(WritableNestedModelSerializer):
    area = AreasSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer()
    user = UserSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Passage
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
            # 'status',
            'images',
            'user',
         ]

    def create(self, validated_data):
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

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            user_fields_for_validation = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Отказано': 'Данные пользователя не могут быть изменены',
                    }
                )
        return data
