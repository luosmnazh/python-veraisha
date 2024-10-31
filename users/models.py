from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    is_driver = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self._before_save()
        super(User, self).save(*args, **kwargs)

    def _before_save(self):
        if self.is_driver:
            self.driver_license = None

        self.username = self.email.split('@')[0]  # username is email without domain


class DriverLicense(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_license', primary_key=True)

    surname = models.CharField(max_length=50)
    name_patronymic = models.CharField(max_length=100)
    iin = models.CharField(max_length=12, unique=True, db_index=True)
    date_of_issue = models.DateField()
    date_of_expiry = models.DateField()
    license_number = models.CharField(max_length=10, unique=True, db_index=True)
    photo = models.ImageField(upload_to='driver_license_photos', null=True, blank=True)
    category = models.ManyToManyField('DriverLicenseCategory')

    def __str__(self):
        return f'{self.surname} {self.name_patronymic} {self.license_number}'


class DriverLicenseCategory(models.Model):
    name = models.CharField(max_length=5, unique=True, db_index=True)
    description = models.TextField()

    def __str__(self):
        return self.name
