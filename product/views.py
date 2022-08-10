from django.shortcuts import render

from basket.forms import AddToBasketForm
from product.models import Product


def product_detail(request, product_slug):
    product = Product.objects.filter(slug=product_slug)
    if product.exists():
        product = product.first()
        form = AddToBasketForm({'product': product, 'quantity': 1})
        return render(request, 'products/product_details.html', {'product': product, "form": form})








