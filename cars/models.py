from django.db import models


# Create your models here.
class Car(models.Model):
    STATUS_TYPES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
    ]

    license_plate = models.CharField(max_length=10)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='available', choices=STATUS_TYPES)
    location = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)  # For internal use only
    model = models.ForeignKey('CarModel', on_delete=models.CASCADE, related_name='cars')

    def __str__(self):
        return f'{self.model} ({self.license_plate})'


class VehicleMaintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    maintenance_date = models.DateField()
    maintenance_description = models.TextField()
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2)


class CarModel(models.Model):
    BODY_TYPES = [
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('suv', 'SUV'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('crossover', 'Crossover'),
    ]

    FUEL_TYPES = [
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    TRANSMISSION_TYPES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(default=2000)
    body_type = models.CharField(max_length=50, choices=BODY_TYPES, default='sedan')
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPES, default='gasoline')
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_TYPES, default='manual')
    default_image = models.ImageField(upload_to='cars/', default='cars/default.jpg', blank=True)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.brand} {self.model}'

    @property
    def get_min_max_price_per_model(self) -> tuple[float, float]:
        """Get the minimum and maximum price for a car model"""
        prices = self.cars.values_list('daily_price', flat=True)
        if prices:
            return min(prices), max(prices)
        return 0, 0

    @property
    def get_availability(self) -> int:
        """Get the number of available cars"""
        return self.cars.filter(status='available').count()

