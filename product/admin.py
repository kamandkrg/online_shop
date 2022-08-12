from django.contrib import admin
from django.contrib.admin import register

from product.models import ProductImage, Product, ProductView, ProductRate


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 2


class ProductRateAdmin(admin.TabularInline):
    model = ProductRate
    extra = 2


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category',  'price', 'amount', 'is_active', 'slug']
    list_filter = ['is_active']
    inlines = [ProductImageAdmin, ProductRateAdmin]


@register(ProductView)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'ip']
