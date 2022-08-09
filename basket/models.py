from django.db import models, transaction
from django.conf import settings
from django.db.models import Sum

from finance.models import Payment
from product.models import Product
from shipping.models import ShippingAddress


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
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='basket_checkout')
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, related_name='basket_checkout', null=True)
    total_price = models.BigIntegerField()

    @staticmethod
    def create_payment(basket, user):
        payment = Payment.object.create(user=user, amount=basket.total_price)
        return payment

    @classmethod
    def create(cls, basket, user, address):
        baskets = Basket.objects.prefetch_related('lines').filter(
            pk=basket.pk).aggregate(total_price=Sum('lines__price')).first()
        with transaction.atomic():
            payment = cls.create_payment(baskets, user)
            basket_checkout = cls.object.create(basket=basket, user=user, payment=payment, address=address,
                                                total_price=baskets.total_price)
        return basket_checkout







