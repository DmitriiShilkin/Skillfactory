from django.db import models
from django.utils import timezone

# список возможных значений статуса для добавления перевала
STATUSES = [
    ('new', 'Новый'),
    ('pending ', 'Модерируется'),
    ('accepted', 'Принят'),
    ('rejected', 'Не принят')
]

# список способов добраться
ACTIVITIES = [
    ('1', 'пешком'),
    ('2', 'лыжи'),
    ('3', 'катамаран'),
    ('4', 'байдарка'),
    ('5', 'плот'),
    ('6', 'сплав'),
    ('7', 'велосипед'),
    ('8', 'автомобиль'),
    ('9', 'мотоцикл'),
    ('10', 'парус'),
    ('11', 'верхом')
]

# список уровней сложности
LEVELS = [
    ('empty', ''),
    ('1a', '1А'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('3b*', '3Б*')
]


def get_image_path(instance, file):
    return f'photos/passage-{instance.passage.id}/{file}'


# Create your models here.
# модель родительских регионов
class ParentAreas(models.Model):
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title


# модель регионов перевалов
class Areas(models.Model):
    title = models.CharField('Название', max_length=255)
    parent = models.ForeignKey(ParentAreas, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# модель географических координат
class Coords(models.Model):
    latitude = models.FloatField('Широта', max_length=32, blank=True, null=True)
    longitude = models.FloatField('Долгота', max_length=32, blank=True, null=True)
    height = models.IntegerField('Высота', blank=True, null=True)


# модель уровней сложности для разных сезонов
class Level(models.Model):
    winter = models.CharField('Зима', choices=LEVELS, max_length=5, default='empty')
    summer = models.CharField('Лето', choices=LEVELS, max_length=5, default='empty')
    autumn = models.CharField('Осень', choices=LEVELS, max_length=5, default='empty')
    spring = models.CharField('Весна', choices=LEVELS, max_length=5, default='empty')


# модель пользователя
class User(models.Model):
    email = models.EmailField('Email', max_length=128)
    phone = models.CharField('Телефон', max_length=12)
    fam = models.CharField('Фамилия', max_length=64)
    name = models.CharField('Имя', max_length=64)
    otc = models.CharField('Отчество', max_length=64, blank=True)


# модель добавления перевала
class Passage(models.Model):
    date_added = models.DateField(default=timezone.now, editable=False)
    beauty_title = models.CharField('Название для рекламы', default='пер. ', max_length=255)
    title = models.CharField('Название', max_length=255)
    other_titles = models.CharField('Другое название', max_length=255, blank=True, null=True)
    connect = models.CharField('Что связывает', max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUSES, default='new')
    spr_activities_types = models.CharField(max_length=2, choices=ACTIVITIES)

    def __str__(self):
        return f'{self.pk}: {self.beauty_title}'


# модель изображений перевала
class Images(models.Model):
    title = models.CharField('Название', max_length=255, blank=True, null=True)
    date_added = models.DateField(default=timezone.now, editable=False)
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    img = models.ImageField('Изображение', upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}: {self.title}'

