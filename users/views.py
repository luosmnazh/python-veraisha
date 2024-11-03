from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserLoginForm, UserRegistrationForm, DriverLicenseForm
from users.mixins import UnauthenticatedOnlyMixin
from users.models import User, DriverLicense


# Create your views here.


class LoginView(UnauthenticatedOnlyMixin, View):
    form_class = UserLoginForm
    success_url = 'cars:index'
    bad_url = 'users:login'
    authenticated_next_page = 'cars:index'

    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        form = self.form_class(request.POST)

        # Check if the form is valid. User matching inside the form
        if not form.is_valid():
            for error in form.errors:
                for message in form.errors[error]:
                    messages.error(request, message, "danger")
            return redirect(self.bad_url)

        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)
        login(request, user)
        return redirect(self.success_url)


class LogoutView(LoginRequiredMixin, View):
    next_page = 'cars:index'

    def get(self, request):
        logout(request)
        return redirect(self.next_page)

    def post(self, request):
        logout(request)
        return redirect(self.next_page)


class RegisterView(UnauthenticatedOnlyMixin, View):
    form_class = UserRegistrationForm
    next_page = 'cars:index'
    authenticated_next_page = 'cars:index'

    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            for error in form.errors:
                for message in form.errors[error]:
                    messages.error(request, message, "danger")
            return redirect('users:register')
        user = form.save()
        login(request, user)
        return redirect(self.next_page)


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html')


class UserDriverLicenseView(LoginRequiredMixin, UpdateView):
    model = DriverLicense
    form_class = DriverLicenseForm
    template_name = 'users/driver_license.html'
    success_url = 'users:profile'

    def get_object(self, queryset=None):
        obj, created = DriverLicense.objects.get_or_create(user=self.request.user)
        return obj
