# Generated by Django 3.0.7 on 2020-06-25 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web_travel_data', '0027_auto_20200622_1159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contribution',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='exeption',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='expence',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='member',
            name='owner',
        ),
        migrations.AlterField(
            model_name='contribution',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web_travel_data.Member', verbose_name='Member'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='note',
            field=models.CharField(default='', max_length=255, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='exeption',
            name='expence',
            field=models.ManyToManyField(to='web_travel_data.Expence', verbose_name='Expence'),
        ),
        migrations.AlterField(
            model_name='exeption',
            name='member',
            field=models.ManyToManyField(to='web_travel_data.Member', verbose_name='Member'),
        ),
        migrations.AlterField(
            model_name='exeption',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Exeption'),
        ),
        migrations.AlterField(
            model_name='exeption',
            name='note',
            field=models.CharField(default='', max_length=255, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='expence',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='expence',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='expence',
            name='note',
            field=models.CharField(default='', max_length=255, verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='expence',
            name='purpose',
            field=models.CharField(max_length=200, verbose_name='Purpose'),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Team name')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contribution',
            name='team',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='web_travel_data.Team'),
        ),
        migrations.AddField(
            model_name='exeption',
            name='team',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='web_travel_data.Team'),
        ),
        migrations.AddField(
            model_name='expence',
            name='team',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='web_travel_data.Team'),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='web_travel_data.Team'),
        ),
    ]
