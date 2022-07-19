from django.db import models
from category.models import Category


class Product(models.Model):
    type = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    amount = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    price = models.PositiveBigIntegerField(default=0)
