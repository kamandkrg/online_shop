from django.contrib import admin

# Register your models here.
from django.contrib.admin import register

from finance.models import Gateway, Payment


@register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable']


@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'amount', 'gateway', 'is_paid', 'user']
