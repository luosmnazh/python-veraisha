from django.contrib import admin

# Register your models here.

from cars.models import Car, VehicleMaintenance, CarModel

admin.site.register(Car)
admin.site.register(VehicleMaintenance)
admin.site.register(CarModel)
