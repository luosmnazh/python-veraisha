from django.db import models

# Create your models here.


class Rental(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    notes = models.TextField()

    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.car} - {self.user}'
