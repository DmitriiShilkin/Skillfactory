# Generated by Django 4.2.2 on 2023-06-10 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0002_alter_level_options_alter_passage_beauty_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='level',
            options={},
        ),
        migrations.AlterField(
            model_name='level',
            name='autumn',
            field=models.CharField(choices=[('empty', 'Не задано'), ('1a', '1А'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b*', '3Б*')], default='empty', max_length=5, verbose_name='Осень'),
        ),
        migrations.AlterField(
            model_name='level',
            name='spring',
            field=models.CharField(choices=[('empty', 'Не задано'), ('1a', '1А'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b*', '3Б*')], default='empty', max_length=5, verbose_name='Весна'),
        ),
        migrations.AlterField(
            model_name='level',
            name='summer',
            field=models.CharField(choices=[('empty', 'Не задано'), ('1a', '1А'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b*', '3Б*')], default='empty', max_length=5, verbose_name='Лето'),
        ),
        migrations.AlterField(
            model_name='level',
            name='winter',
            field=models.CharField(choices=[('empty', 'Не задано'), ('1a', '1А'), ('1b', '1Б'), ('2a', '2А'), ('2b', '2Б'), ('3a', '3А'), ('3b', '3Б'), ('3b*', '3Б*')], default='empty', max_length=5, verbose_name='Зима'),
        ),
        migrations.AlterField(
            model_name='passage',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pereval.areas'),
        ),
        migrations.AlterField(
            model_name='passage',
            name='beauty_title',
            field=models.CharField(default='пер.', max_length=255, verbose_name='Префикс'),
        ),
        migrations.AlterField(
            model_name='passage',
            name='spr_activities_types',
            field=models.CharField(choices=[('empty', 'Не задано'), ('1', 'пешком'), ('2', 'лыжи'), ('3', 'катамаран'), ('4', 'байдарка'), ('5', 'плот'), ('6', 'сплав'), ('7', 'велосипед'), ('8', 'автомобиль'), ('9', 'мотоцикл'), ('10', 'парус'), ('11', 'верхом')], default='empty', max_length=5, verbose_name='На чем добраться'),
        ),
        migrations.AlterField(
            model_name='user',
            name='otc',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Отчество'),
        ),
    ]
