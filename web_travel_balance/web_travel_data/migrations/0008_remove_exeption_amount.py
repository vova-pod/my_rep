# Generated by Django 3.0.7 on 2020-06-11 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_travel_data', '0007_exeption_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exeption',
            name='amount',
        ),
    ]
