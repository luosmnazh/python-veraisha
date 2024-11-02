from cars.models import Car, CarModel


def get_random_car_by_model_id(model_id: int) -> Car | None:
    """Get a random car by model id"""
    return Car.objects.filter(model_id=model_id, status='available').order_by('?').first()


def set_car_status(car: Car, status: str) -> None:
    """Mark a car as available or unavailable"""
    car.status = status
    car.save()
