from django.conf import settings
from django.db import models
from django.db.models import Avg

from category.models import Category


class Product(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0)
    sale_number = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/")
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)


class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='visits')
    ip = models.GenericIPAddressField()

    @classmethod
    def increase_visit(cls, product, ip):
        product_exist = cls.objects.filter(product=product)
        if product_exist.exists():
            ip_address = product_exist.filter(ip=ip)
            if ip_address.exists():
                return
        cls.objects.create(product=product, ip=ip)


class ProductRate(models.Model):
    rate = models.PositiveSmallIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rates')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates')

    @classmethod
    def avg(cls, product):
        avg = cls.objects.filter(product=product).aggregate(avg_rate=Avg('rate'))
        return avg.get('avg_rate')


