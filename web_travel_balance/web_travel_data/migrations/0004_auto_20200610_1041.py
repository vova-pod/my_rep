# Generated by Django 3.0.7 on 2020-06-10 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_travel_data', '0003_expence'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='balance',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='contribute',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]