from django.db import models
from django.utils import timezone

# список возможных значений статуса для добавления перевала
STATUSES = [
    ('new', 'Новый'),
    ('pending ', 'Модерируется'),
    ('accepted', 'Принят'),
    ('rejected', 'Не принят')
]

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


# Create your models here.
# модель родительских регионов
class ParentAreas(models.Model):
    title = models.CharField(max_length=255)


# модель регионов перевалов
class PerevalAreas(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(ParentAreas, on_delete=models.CASCADE)


# модель фотографий перевалов
class PerevalImages(models.Model):
    title = models.CharField(max_length=255)
    date_added = models.DateField(default=timezone.now(), editable=False)
    img = models.BinaryField()


# модель добавления перевала
class PerevalAdded(models.Model):
    date_added = models.DateField(default=timezone.now(), editable=False)
    raw_data = models.JSONField()
    images = models.ForeignKey(PerevalImages, on_delete=models.CASCADE)
    area = models.ForeignKey(PerevalAreas, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUSES, default='new')
    spr_activities_types = models.CharField(max_length=2, choices=ACTIVITIES)
