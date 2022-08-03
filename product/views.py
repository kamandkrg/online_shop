from django.shortcuts import render


def product_list(request):
    return render(request, 'home/register.html')


def product_detail(request, product_slug):
    pass









