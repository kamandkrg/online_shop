from django.db.models import Q
from django.shortcuts import render

from category.models import Category
from product.models import Product


def show_all(request):
    pass


def show_detail(request, slug_category):
    context = dict()
    category = Category.objects.get(slug=slug_category)
    products = Product.objects.filter(Q(category=category) | Q(category__parent=category))
    context['products'] = products
    return render(request, 'products/product_category.html', context=context)


