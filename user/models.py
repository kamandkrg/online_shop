from django.db import models


class User(models.Model):
    SEX = (
        ("M", "Male"),
        ("F", "Female"),
    )
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX)
    number = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=122, unique=True)
    password = models.CharField(max_length=122)


