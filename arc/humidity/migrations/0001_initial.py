# Generated by Django 3.2.4 on 2021-07-01 04:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exhaust',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.TextField(default='')),
                ('status', models.TextField(default='')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='HumidityTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humidity', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('temp', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='HumidityTempValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('humidity_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('buffer_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('temp_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
