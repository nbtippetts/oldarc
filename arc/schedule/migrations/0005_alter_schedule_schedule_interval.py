# Generated by Django 3.2.4 on 2021-08-01 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20210731_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='schedule_interval',
            field=models.TextField(default=''),
        ),
    ]
