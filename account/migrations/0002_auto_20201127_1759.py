# Generated by Django 3.1.3 on 2020-11-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
