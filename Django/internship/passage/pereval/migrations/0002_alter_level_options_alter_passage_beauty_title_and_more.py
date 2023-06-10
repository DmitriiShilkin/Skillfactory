# Generated by Django 4.2.2 on 2023-06-09 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='level',
            options={'verbose_name': 'Уровень сложности', 'verbose_name_plural': 'Уровни сложности'},
        ),
        migrations.AlterField(
            model_name='passage',
            name='beauty_title',
            field=models.CharField(default='пер. ', max_length=255, verbose_name='Префикс'),
        ),
        migrations.AlterField(
            model_name='passage',
            name='spr_activities_types',
            field=models.CharField(choices=[('1', 'пешком'), ('2', 'лыжи'), ('3', 'катамаран'), ('4', 'байдарка'), ('5', 'плот'), ('6', 'сплав'), ('7', 'велосипед'), ('8', 'автомобиль'), ('9', 'мотоцикл'), ('10', 'парус'), ('11', 'верхом')], max_length=2, verbose_name='На чем добраться'),
        ),
        migrations.AlterField(
            model_name='passage',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('pending ', 'Модерируется'), ('accepted', 'Принят'), ('rejected', 'Не принят')], default='new', max_length=8, verbose_name='Статус'),
        ),
    ]
