from django.db import models
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
    slug = models.SlugField(max_length=255, unique=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/")
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)
