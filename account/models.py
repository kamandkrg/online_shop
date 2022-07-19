from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from account.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unsure')
    )
    name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=40, unique=True)
    username = models.CharField(unique=True, max_length=32)
    data_join = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICE, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']












