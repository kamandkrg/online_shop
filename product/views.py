from django.shortcuts import render

from basket.forms import AddToBasketForm
from product.models import Product, ProductView


def product_detail(request, product_slug):
    product = Product.objects.filter(slug=product_slug)
    if product.exists():
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')
        product = product.first()
        ProductView.increase_visit(product, ipaddress)
        form = AddToBasketForm({'product': product, 'quantity': 1})
        return render(request, 'products/product_details.html', {'product': product, "form": form})








