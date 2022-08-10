from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from basket.models import BasketCheckout
from finance.models import Payment


@receiver(post_save, sender=Payment)
def verify_callback(sender, instance, created, **kwargs):
    if instance.is_paid:
        basket_check = instance.basket_checkout.first()
        basket_check.status = BasketCheckout.PAID
        basket_check.save()
        basket = basket_check.basket
        basket.sale_product()
