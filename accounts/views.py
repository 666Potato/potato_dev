from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
# Create your views here.

from .forms import LoginForm


def login_view(request):
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)
        redirect('/')
        
        context = {
            'form': form
        }

        return render(request, 'accounts:login.html', context)
