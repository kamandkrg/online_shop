from django.db import models
from django.conf import settings

from product.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='baskets')
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)


class BasketLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lines')
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='lines')
    quantity = models.PositiveSmallIntegerField()


class BasketCheckout(models.Model):
    PAID = 10
    NOT_PAID = -10
    STATUS_CHOICE = (
        (PAID, 'paid'),
        (NOT_PAID, 'not paid'),
    )

    status = models.SmallIntegerField(choices=STATUS_CHOICE, default=NOT_PAID)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_checkout')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket_checkout')








