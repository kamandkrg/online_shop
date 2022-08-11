from django.contrib import admin
from django.contrib.admin import register

from product.models import ProductImage, Product, ProductView


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 2


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category',  'price', 'amount', 'is_active', 'slug']
    list_filter = ['is_active']
    inlines = [ProductImageAdmin]


@register(ProductView)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'ip']
