from django.shortcuts import render


# Create your views here.


def user_login(request):
    return render(request, 'users/login.html')


def user_logout(request):
    return render(request, 'users/logout.html')


def user_register(request):
    return render(request, 'users/register.html')
