# Generated by Django 5.1.2 on 2024-11-02 03:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('default_image', models.ImageField(blank=True, default='cars/default.jpg', upload_to='cars/')),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.RemoveField(
            model_name='car',
            name='mark',
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars',
                                    to='cars.carmodel'),
        ),
    ]
