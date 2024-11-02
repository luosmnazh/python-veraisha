from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from cars.forms import CarCreateForm, CarModelForm, VehicleMaintenanceForm
from cars.models import Car, CarModel, VehicleMaintenance
from rent.models import Rental
from users.models import User


# Create your views here.

class IndexPageView(TemplateView):
    template_name = 'cars/index.html'


class CarModelListView(LoginRequiredMixin, ListView):
    model = CarModel
    template_name = 'cars/car_models.html'
    context_object_name = 'car_models'


class CarListView(ListView):
    model = Car
    template_name = 'cars/cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        model = get_object_or_404(CarModel, pk=model_id)
        return Car.objects.filter(model=model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars_by_model'] = self.get_queryset()
        return context


def filter_cars(request):
    """Supported filters: body_type"""
    body_types = request.GET.getlist('body_type')
    if body_types:
        cars = Car.objects.filter(body_type__in=body_types)
    else:
        cars = Car.objects.all()
    return render(request, 'cars/filter_cars.html', {'cars': cars})


class CarCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Car
    form_class = CarCreateForm
    success_url = reverse_lazy('cars:car_models')
    permission_required = 'cars.add_car'
    template_name = 'cars/car_add.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['car_model_form'] = CarModelForm(self.request.POST, self.request.FILES)
        else:
            data['car_model_form'] = CarModelForm()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        car_model_form = context['car_model_form']

        if form.cleaned_data['model']:
            car = form.save(commit=False)
            car.model = form.cleaned_data['model']
        elif car_model_form.is_valid():
            car_model = car_model_form.save()
            car = form.save(commit=False)
            car.model = car_model
        else:
            return self.form_invalid(form)

        car.save()
        return redirect(self.success_url)


class CarUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'cars/car_update.html'
    success_url = reverse_lazy('cars:cars')
    permission_required = 'cars.change_car'
    login_url = reverse_lazy('users:login')


class CarMaintenancesView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = VehicleMaintenance
    permission_required = 'cars.change_car'
    login_url = reverse_lazy('users:login')
    template_name = 'cars/car_maintenance.html'
    context_object_name = 'maintenances'

    def get_queryset(self):
        car = get_object_or_404(Car, pk=self.kwargs.get('pk'))
        return VehicleMaintenance.objects.filter(car=car)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        car = get_object_or_404(Car, pk=self.kwargs.get('pk'))
        context['car'] = car
        return context


class CarMaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = VehicleMaintenance
    form_class = VehicleMaintenanceForm
    template_name = 'cars/car_maintenance_create.html'
    success_url = 'cars:car_list_manager'
    permission_required = 'cars.change_car'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = get_object_or_404(Car, pk=self.kwargs.get('pk'))
        context['car'] = car
        return context

    def form_valid(self, form):
        car = get_object_or_404(Car, pk=self.kwargs.get('pk'))

        maintenance = form.save(commit=False)
        maintenance.car = car
        maintenance.save()
        return redirect(self.success_url, model_id=car.model.pk)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class CarDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'cars.delete_car'
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return redirect('cars:car_list_manager', model_id=car.model.pk)

    def post(self, request, pk):
        return self.get(request, pk)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'cars/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars_in_rent'] = Car.objects.filter(status='rented').count()
        context['cars_in_service'] = Car.objects.filter(status='in_service').count()
        context['total_cars'] = Car.objects.count()
        context['total_car_models'] = CarModel.objects.count()
        context['total_maintenance'] = VehicleMaintenance.objects.count()
        context['total_users'] = User.objects.count()
        context['total_maintenance_cost'] = VehicleMaintenance.objects.aggregate(total_cost=Sum('maintenance_cost'))['total_cost'] or 0
        context['total_rental_income'] = Rental.objects.filter(status='finished').aggregate(total_income=Sum('total_price'))['total_income'] or 0
        return context
