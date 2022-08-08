from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from account.forms import UserLoginForm, UserRegisterForm
from account.models import User


@require_http_methods(request_method_list=["POST", "GET"])
def sing_up(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home-page')
        return redirect('register')
    else:
        form = UserRegisterForm()
        return render(request, 'home/register.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect("home-page")


@require_http_methods(request_method_list=['POST', 'GET'])
def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home-page')
        return redirect('login')
    else:
        form = UserLoginForm()
        return render(request, 'home/login.html', {'form': form})
