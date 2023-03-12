from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from users.forms import UserRegistrationForm
# Create your views here.

def index(request):
    return render(request, 'users/index.html')

def registration(request):
    if request.user.is_authenticated:
        return redirect(index)
    
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            login(request, user)
            messages.success(request, f"Hello <b>{user.username}</b>, your account has been created.")
            return redirect(index)
        else:
            for error in list(registration_form.errors.values()):
                messages.error(request, error)
                return redirect(registration)
    else:
        registration_form = UserRegistrationForm()
        context = {'registration_form':registration_form}
        return render(request, 'users/registration.html', context)


def custom_login(request):
    login_form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect(index)

    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"welcome back <b>{user.username}</b>")
                return redirect(index)
        else:
            for error in list(login_form.errors.values()):
                messages.error(request, error)
                return redirect(custom_login)

    context = {'login_form':login_form}
    return render(request, 'users/login.html', context)


@login_required
def custom_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'users/logout.html')
    else:
        return redirect(custom_login)
