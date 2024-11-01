from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from cars.services import get_random_car_by_model_id, set_car_status
from rent.forms import RentalCreateForm
from rent.models import Rental
from users.models import User


def rent_car(model_id: int, user: User, form: RentalCreateForm) -> RentalCreateForm:
    """Rent a car"""
    car = get_random_car_by_model_id(model_id)
    form.instance.user = user
    form.instance.car = car
    form.instance.status = 'active'
    set_car_status(car, car.STATUS_TYPES[1][0])

    return form.save(commit=False)


def cancel_rent(rental: Rental, request) -> None:
    """Cancel a rental"""
    if rental.status == 'In progress':
        messages.error(request,
                       'You cannot cancel a rental in progress. Please follow to closest facility to return the car.')
        return
    if rental.status == 'Cancelled':
        messages.error(request, 'This rental is already cancelled.')
        return
    rental.status = 'Cancelled'
    rental.end_date = rental.start_date
    set_car_status(rental.car, 'available')
    rental.save()


def finish_rent(rental: Rental) -> None:
    """Finish a rental"""
    if rental.status == 'Cancelled':
        raise ValueError('You cannot finish a cancelled rental. Maybe you want to cancel it?')
    rental.status = 'Finished'
    rental.save()
    set_car_status(rental.car, 'available')
    rental.car.save()
