from django.db.models.signals import pre_save, post_save, post_init
from django.dispatch import receiver

from basket.models import BasketCheckout
from finance.models import Payment


@receiver(post_save, sender=Payment)
def verify_callback(sender, instance, created, **kwargs):
    if instance.is_paid and not instance._b_is_paid:
        basket_check = instance.basket_checkout.first()
        basket_check.status = BasketCheckout.PAID
        basket_check.save()
        basket = basket_check.basket
        basket.sale_product()


@receiver(post_init, sender=Payment)
def store_is_paid_status(sender, instance, **kwargs):
    instance._b_is_paid = instance.is_paid
