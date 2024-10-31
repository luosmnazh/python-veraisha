from django.contrib import admin

# Register your models here.

from .models import User, DriverLicense, DriverLicenseCategory

admin.site.register(User)
admin.site.register(DriverLicense)
admin.site.register(DriverLicenseCategory)