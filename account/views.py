from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def registration_form_view(request):
    context = {}
    form = RegistrationForm()
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    print(form)
    context['form'] = form
    return render(request, 'account/registration.html', context)


def login_form_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('store')

    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('store')
            else:
                form.add_error(None, "Could not log the user in")
    context['form'] = form
    return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('store')
