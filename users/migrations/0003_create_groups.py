# Generated by Django 5.1.2 on 2024-11-02 00:41

from django.db import migrations, transaction


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    Car = apps.get_model('cars', 'Car')

    content_type = ContentType.objects.get_for_model(Car)
    permissions = Permission.objects.filter(content_type=content_type)

    with transaction.atomic():
        managers = Group.objects.create(name='Car manager')
        managers.permissions.set(permissions)

        admin = Group.objects.create(name='Admin')
        admin.permissions.set(permissions)


def delete_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    with transaction.atomic():
        Group.objects.filter(name='Car manager').delete()
        Group.objects.filter(name='Admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_driverlicensecategory_user_is_driver_driverlicense'),
    ]

    operations = [
        migrations.RunPython(code=create_groups, reverse_code=delete_groups),
    ]
