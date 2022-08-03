from django.shortcuts import render

from product.models import Product


def product_detail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    return render(request, 'products/product_details.html', {'product': product})








