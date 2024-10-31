from cars.models import Car, CarModel


def get_random_car_by_model(model: CarModel) -> Car | None:
    """Get a random car by model"""
    return Car.objects.filter(model__model=model).order_by('?').first()
