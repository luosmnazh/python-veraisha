# Generated by Django 5.1.2 on 2024-11-06 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_create_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverlicense',
            name='date_of_expiry',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='date_of_issue',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='iin',
            field=models.CharField(db_index=True, default='', max_length=12),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='license_number',
            field=models.CharField(db_index=True, default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='name_patronymic',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='photo',
            field=models.ImageField(blank=True, default='', null=True, upload_to='driver_license_photos'),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='surname',
            field=models.CharField(default='', max_length=50),
        ),
    ]
