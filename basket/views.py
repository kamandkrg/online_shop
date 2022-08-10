from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from basket.forms import AddToBasketForm
from basket.models import Basket, BasketLine, BasketCheckout
from finance.models import Gateway
from shipping.forms import ShippingAddressForm


@require_POST
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


@require_http_methods(request_method_list=["GET"])
def show_basket(request):
    basket_id = request.COOKIES.get('basket_id', None)
    basket = Basket.get_basket(basket_id)
    lines, total_all = BasketLine.show_lines(basket)
    return render(request, 'basket/cart.html', context={'lines': lines, 'total_all': total_all})


@require_http_methods(request_method_list=['GET'])
def delete_item(request, pk):
    basket_id = request.COOKIES.get('basket_id', None)
    basket = Basket.get_basket(basket_id)
    item = basket.lines.filter(pk=pk)
    if item.exists():
        item.delete()
    return redirect('show-basket')


@login_required(login_url='login')
@require_http_methods(request_method_list=['GET', 'POST'])
def basket_checkout(request):
    basket_id = request.COOKIES.get('basket_id', None)
    basket = Basket.get_basket(basket_id)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance = form.save()
            basket_check = BasketCheckout.create(basket, request.user, instance)
            gateway = Gateway.objects.get(pk=request.POST.get('gate-code'))
            basket_check.payment.gateway = gateway
            link = basket_check.payment.bank_page
            return redirect(link)
    else:
        form = ShippingAddressForm()
        gateway = Gateway.objects.all()
        lines, total_all = BasketLine.show_lines(basket)
        return render(request, 'basket/shipping_cart.html', context={'form': form, 'gateway': gateway,
                                                                     'total_all': total_all})

