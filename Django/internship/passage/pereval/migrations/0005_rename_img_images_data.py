# Generated by Django 4.2.2 on 2023-06-10 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0004_alter_passage_connect'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='img',
            new_name='data',
        ),
    ]
