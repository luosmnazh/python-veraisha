# Generated by Django 5.1.2 on 2024-10-31 06:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_default_driver_license_category(apps, schema_editor):
    DriverLicenseCategory = apps.get_model('users', 'DriverLicenseCategory')
    DriverLicenseCategory.objects.bulk_create([
        DriverLicenseCategory(name="B", description="Cars, small vans up to 3.5 tonnes. Can tow trailers up to 750kg."),
        DriverLicenseCategory(name="B1",
                              description="Tricycles, quadricycles, motorcycles with sidecar. Minimum age 18."),
        DriverLicenseCategory(name="C",
                              description="Goods vehicles over 3.5 tonnes. Minimum age 21, 3 years driving experience."),
        DriverLicenseCategory(name="C1", description="Medium-sized goods vehicles (3.5-7.5 tonnes). Minimum age 18."),
    ])


def delete_default_driver_license_category(apps, schema_editor):
    DriverLicenseCategory = apps.get_model('users', 'DriverLicenseCategory')
    DriverLicenseCategory.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverLicenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=5, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_driver',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='DriverLicense',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True,
                                              related_name='driver_license', serialize=False,
                                              to=settings.AUTH_USER_MODEL)),
                ('surname', models.CharField(max_length=50)),
                ('name_patronymic', models.CharField(max_length=100)),
                ('iin', models.CharField(db_index=True, max_length=12, unique=True)),
                ('date_of_issue', models.DateField()),
                ('date_of_expiry', models.DateField()),
                ('license_number', models.CharField(db_index=True, max_length=10, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='driver_license_photos')),
                ('category', models.ManyToManyField(to='users.driverlicensecategory')),
            ],
        ),
        migrations.RunPython(code=create_default_driver_license_category,
                             reverse_code=delete_default_driver_license_category),
    ]
