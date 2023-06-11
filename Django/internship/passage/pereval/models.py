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
    ('', 'Не задано'),
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
    ('', 'Не задано'),
    ('1a', '1А'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('3b*', '3Б*')
]


# функция получения пути для сохранения фотографий, чтобы было понятно, к какому перевалу они относятся
def get_image_path(instance, file):
    return f'photos/pereval-{instance.passage.id}/{file}'


# Create your models here.
'''
модель родительских регионов (горных систем), нужно предварительно добавить в БД;
значения брались из примера структуры БД ФСТР;
SQL-запрос, который я выполнил для своей БД:
INSERT INTO "public"."pereval_parentareas" ("id", "title") VALUES
(0, 'Планета Земля'),
(1, 'Памиро-Алай'),
(65, 'Алтай'),
(375, 'Тавр'),
(384, 'Саяны');
'''


class ParentAreas(models.Model):
    title = models.CharField('Название', max_length=255)

    def __str__(self):
        return self.title


'''
модель регионов перевалов (горных систем), перед созданием перевала нужно предварительно добавить данные в БД,
связать их с родительскими регионами, чтобы в соответствующем поле HTML-формы был выпадающий список со
значениями;
значения брались из примера структуры БД ФСТР;
SQL-запрос, который я выполнил для своей БД:
INSERT INTO "public"."pereval_areas" ("id", "parent_id", "title") VALUES
(1, 0, 'Не задано'),
(66, 65, 'Северо-Чуйский хребет'),
(88, 65, 'Южно-Чуйский хребет'),
(92, 65, 'Катунский хребет'),
(105, 1, 'Фанские горы'),
(106, 1, 'Гиссарский хребет (участок западнее перевала Анзоб)'),
(131, 1, 'Матчинский горный узел'),
(133, 1, 'Горный узел Такали, Туркестанский хребет'),
(137, 1, 'Высокий Алай'),
(147, 1, 'Кичик-Алай и Восточный Алай'),
(367, 375, 'Аладаглар'),
(386, 65, 'Хребет Листвяга'),
(387, 65, 'Ивановский хребет'),
(388, 65, 'Массив Мунгун-Тайга'),
(389, 65, 'Хребет Цаган-Шибэту'),
(390, 65, 'Хребет Чихачева (Сайлюгем)'),
(391, 65, 'Шапшальский хребет'),
(392, 65, 'Хребет Южный Алтай'),
(393, 65, 'Хребет Монгольский Алтай'),
(398, 384, 'Западный Саян'),
(399, 384, 'Восточный Саян'),
(402, 384, 'Кузнецкий Алатау'),
(459, 65, 'Курайский хребет');
'''


class Areas(models.Model):
    title = models.CharField('Название', max_length=255)
    parent = models.ForeignKey(ParentAreas, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


# модель географических координат
class Coords(models.Model):
    latitude = models.FloatField('Широта', max_length=32, blank=True, null=True)
    longitude = models.FloatField('Долгота', max_length=32, blank=True, null=True)
    height = models.IntegerField('Высота', blank=True, null=True)

    def __str__(self):
        return f'широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}'


# модель уровней сложности для разных сезонов
class Level(models.Model):
    winter = models.CharField('Зима', choices=LEVELS, max_length=5, default='')
    summer = models.CharField('Лето', choices=LEVELS, max_length=5, default='')
    autumn = models.CharField('Осень', choices=LEVELS, max_length=5, default='')
    spring = models.CharField('Весна', choices=LEVELS, max_length=5, default='')

    def __str__(self):
        return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, весна: {self.spring}'


# модель пользователя
class User(models.Model):
    email = models.EmailField('Email', max_length=128)
    phone = models.CharField('Телефон', max_length=12)
    fam = models.CharField('Фамилия', max_length=64)
    name = models.CharField('Имя', max_length=64)
    otc = models.CharField('Отчество', max_length=64, blank=True, null=True)

    def __str__(self):
        return f'{self.fam} {self.name} {self.otc}'


# модель добавления перевала
class Passage(models.Model):
    date_added = models.DateField(default=timezone.now, editable=False)
    beauty_title = models.CharField('Префикс', default='пер.', max_length=255)
    title = models.CharField('Название', max_length=255)
    other_titles = models.CharField('Другое название', max_length=255, blank=True, null=True)
    connect = models.TextField('Что соединяет', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE, default=1)
    status = models.CharField('Статус', max_length=8, choices=STATUSES, default='new')
    spr_activities_types = models.CharField('На чем добраться', max_length=5, choices=ACTIVITIES, default='')

    def __str__(self):
        return f'{self.pk}: {self.beauty_title} {self.title}'


# модель изображений перевала
class Images(models.Model):
    title = models.CharField('Название', max_length=255, blank=True, null=True)
    date_added = models.DateField(default=timezone.now, editable=False)
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    img = models.ImageField('Изображение', upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}: {self.title} {self.img}'
