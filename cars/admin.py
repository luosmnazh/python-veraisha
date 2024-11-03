from django.contrib import admin

from cars.models import Car, VehicleMaintenance, CarModel

# Register your models here.

admin.site.register(Car)
admin.site.register(VehicleMaintenance)
admin.site.register(CarModel)
