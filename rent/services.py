from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from cars.services import get_random_car_by_model_id, set_car_status
from rent.forms import RentalCreateForm
from rent.models import Rental
from users.models import User


def rent_car(model_id: int, user: User, form: RentalCreateForm, request) -> Rental | None:
    """Rent a car"""
    car = get_random_car_by_model_id(model_id)
    if not car:
        messages.error(request, 'No cars available for this model. How did you get here?')
        return

    if user.rentals.filter(status='pending').exists():
        messages.error(request, 'You already have a pending rental')
        return

    form.instance.user = user
    form.instance.car = car
    form.instance.status = 'pending'
    set_car_status(car, car.STATUS_TYPES[1][0])

    return form.save(commit=False)


def cancel_rent(rental: Rental, request) -> None:
    """Cancel a rental"""
    if rental.status != 'pending':
        messages.error(request, 'You can only cancel pending rentals')
        return
    rental.status = 'cancelled'
    rental.end_date = rental.start_date
    set_car_status(rental.car, 'available')
    rental.save()


def finish_rent(rental: Rental, request) -> None:
    """Finish a rental"""
    if rental.status == 'cancelled':
        messages.error(request, 'You can only finish active rentals')
        return
    rental.status = 'finished'
    rental.save()
    set_car_status(rental.car, 'available')
    rental.car.save()
