# Generated by Django 3.0.7 on 2020-06-18 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_travel_data', '0014_auto_20200617_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='exeption',
            name='i',
            field=models.IntegerField(default=0),
        ),
    ]
