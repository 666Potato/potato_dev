from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .forms import LoginForm, RegisterForm


def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('lessons:index')

        else:
            return render(request, 'accounts/login.html',
                          context={'form': LoginForm(), 'error': 'Логин и пароль не совпали'})

    else:
        return render(request, 'accounts/login.html', context={'form': LoginForm()})


def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('lessons:index')

    else:
        form = RegisterForm()

    return render(request, 'accounts/registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('lessons:index')
