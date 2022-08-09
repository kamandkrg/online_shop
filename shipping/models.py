from django.conf import settings
from django.db import models


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=32, blank=True)
    address = models.TextField()
    zipcode = models.CharField(max_length=16)
    number = models.PositiveSmallIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.zipcode)

    @classmethod
    def get_addresses(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def add_address(cls, user, city, address, zipcode, number):
        instance = cls.objects.create(user=user, city=city, address=address, zipcode=zipcode, number=number)
        return instance
