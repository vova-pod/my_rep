# Generated by Django 3.0.7 on 2020-06-18 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_travel_data', '0015_exeption_i'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='note',
            field=models.TextField(default=''),
        ),
    ]
