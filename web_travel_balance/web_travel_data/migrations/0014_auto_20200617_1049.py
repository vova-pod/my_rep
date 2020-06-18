# Generated by Django 3.0.7 on 2020-06-17 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_travel_data', '0013_contribution_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='i',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
