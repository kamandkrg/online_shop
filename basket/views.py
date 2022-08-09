from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from basket.forms import AddToBasketForm
from basket.models import Basket


def add_to_basket(request):
    response = HttpResponseRedirect(request.POST.get('next', '/'))
    basket_id = request.COOKIES.get('basket_id', None)
    basket = Basket.get_basket(basket_id)
    if basket is None:
        return Http404

    response.set_cookie('basket_id', basket.id)

    if not basket.check_authenticate(request.user):
        return Http404

    form = AddToBasketForm(request.POST)
    if form.is_valid():
        form.save(basket=basket)

    return response


def show_basket(request):
    pass
