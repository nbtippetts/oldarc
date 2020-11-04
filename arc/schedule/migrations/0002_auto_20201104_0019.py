# Generated by Django 3.1 on 2020-11-04 00:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='relay',
            name='relay_finish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='relay',
            name='relay_start',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]