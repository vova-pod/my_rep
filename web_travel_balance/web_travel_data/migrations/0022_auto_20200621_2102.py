# Generated by Django 3.0.7 on 2020-06-21 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_travel_data', '0021_exeption_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web_travel_data.Member'),
        ),
        migrations.AlterField(
            model_name='expence',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]