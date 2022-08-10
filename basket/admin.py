from django.contrib import admin
from django.contrib.admin import register

from basket.models import Basket, BasketLine, BasketCheckout


class BasketLineTabular(admin.TabularInline):
    model = BasketLine


@register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_time', 'modify_time']
    inlines = [BasketLineTabular]


@register(BasketCheckout)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['status', 'user', 'payment', 'total_price']
