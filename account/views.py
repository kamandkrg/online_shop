from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_GET
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from account.serializers import CreateUserSerializers, UpdateUserSerializer, UpdateDestroyRetrieveUserSerializer
from lib.permissions import HaveUpdatePermission, NotAuthenticatePermission

from account.forms import UserLoginForm, UserRegisterForm
from account.models import User
from basket.models import BasketCheckout


class SingUpAPIView(ListCreateAPIView):
    serializer_class = CreateUserSerializers
    queryset = User.objects.all()
    permission_classes = (NotAuthenticatePermission, )


class UpdatePasswordUserAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated, HaveUpdatePermission)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        if self.kwargs.get('pk', None) and (self.request.user.is_staff or self.request.user.is_superuser):
            return super(UpdatePasswordUserAPIView, self).get_object()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (IsAuthenticated, HaveUpdatePermission)
        return [permission() for permission in permission_classes]


class UpdateUserAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateDestroyRetrieveUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        if self.kwargs.get('pk', None) and (self.request.user.is_staff or self.request.user.is_superuser):
            return super(UpdateUserAPIView, self).get_object()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (IsAuthenticated, HaveUpdatePermission)
        return [permission() for permission in permission_classes]


class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        print(token)
        token.blacklist()
        return Response(f"Success")


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


@login_required
@require_GET
def profile(request):
    basket = BasketCheckout.objects.filter(user=request.user).prefetch_related('basket')
    return render(request, 'profile/profile.html', {'basket': basket})











