from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
                               max_length=200)
    password = forms.CharField(widget=forms.PasswordInput(
                               attrs={'class': 'form-control', 'placeholder': 'Введите ваш пароль'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=30)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
