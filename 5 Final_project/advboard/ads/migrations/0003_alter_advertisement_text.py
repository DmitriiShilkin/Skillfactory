# Generated by Django 3.2 on 2023-05-28 20:59

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_advertisement_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
