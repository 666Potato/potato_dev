from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
# Create your views here.

from .forms import LoginForm


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if request.method == 'POST':
        if user is not None:
            login(request, user)
            return redirect('lessons:index')

        if not user:
            raise ValueError('Логин и пароль не совпали')

    else:
        return render(request, 'accounts/login.html', context={'form': LoginForm()})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
