from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from cars.services import get_random_car_by_model_id
from rent.forms import RentalCreateForm
from rent.models import Rental
from rent.services import rent_car, cancel_rent
from users.mixins import GroupRequiredMixin


# Create your views here.


class RentalUserListView(LoginRequiredMixin, ListView):
    model = Rental
    template_name = 'rent/rental_user_list.html'
    context_object_name = 'rentals'

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)


class RentalManagerListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = Rental
    template_name = 'rent/rental_manager_list.html'
    context_object_name = 'rentals'
    group_required = ['Car manager', 'Admin']

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return Rental.objects.filter(user_id=user_id)
        return Rental.objects.all()


class RentalCreateView(LoginRequiredMixin, CreateView):
    model = Rental
    form_class = RentalCreateForm
    template_name = 'rent/rental_form.html'
    success_url = 'rental_detail'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if not form.is_valid():
            messages.error(self.request, form.errors)
            return self.form_invalid(form)

        form = rent_car(self.kwargs.get('model_id'), self.request.user, form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('rent:rental_detail', kwargs={'pk': self.object.pk})


class RentalCancelView(LoginRequiredMixin, View):
    def get(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        cancel_rent(rental, request)
        return redirect('rent:rental_detail', pk=pk)


class RentalFinishView(LoginRequiredMixin, View):
    def get(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk)
        if rental.status == 'Cancelled':
            messages.error(request, 'You cannot finish a cancelled rental. Maybe you want to cancel it?')
        else:
            rental.status = 'Finished'
            rental.save()
        return redirect('rent:rental_detail', pk=pk)


class RentalDetailView(LoginRequiredMixin, DetailView):
    model = Rental
    template_name = 'rent/rental_detail.html'
    context_object_name = 'rental'
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental'] = get_object_or_404(Rental, pk=self.kwargs.get('pk'))
        return context




