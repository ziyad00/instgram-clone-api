# Generated by Django 3.1.3 on 2021-01-11 13:55

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='users/%Y/%m/%d/'),
        ),
    ]
