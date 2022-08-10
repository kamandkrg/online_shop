from django.db import models, transaction
from django.conf import settings
from django.db.models import Sum, F

from finance.models import Payment
from product.models import Product
from shipping.models import ShippingAddress


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='baskets')
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    def add(self, product, quantity):

        if self.lines.filter(product=product).exists():
            line = self.lines.filter(product=product).first()
            line.quantity += quantity
            line.save()
        else:
            line = self.lines.create(product=product, quantity=quantity)
        return line

    @classmethod
    def get_basket(cls, basket_id):
        if basket_id is None:
            basket = cls.objects.create()
        else:
            try:
                basket = cls.objects.get(pk=basket_id)
            except cls.DoseNotExist:
                basket = None
        return basket

    def check_authenticate(self, user):
        if user.is_authenticated:
            if self.user is not None and user != self.user:
                return False
            if self.user is None:
                self.user = user
                self.save()
        elif self.user is not None:
            return False
        return True


class BasketLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lines')
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='lines')
    quantity = models.PositiveSmallIntegerField()

    @classmethod
    def show_lines(cls, basket):
        related = cls.objects.prefetch_related('product').filter(basket=basket)
        lines = related.annotate(total=F('quantity') * F('product__price'))
        return lines


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







