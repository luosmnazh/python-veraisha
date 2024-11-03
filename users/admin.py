from django.contrib import admin

from .models import User, DriverLicense, DriverLicenseCategory

# Register your models here.

admin.site.register(User)
admin.site.register(DriverLicense)
admin.site.register(DriverLicenseCategory)
