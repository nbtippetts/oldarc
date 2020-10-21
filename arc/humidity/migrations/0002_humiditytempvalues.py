# Generated by Django 3.1 on 2020-09-20 16:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('humidity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumidityTempValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humidity_value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('temp_value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]