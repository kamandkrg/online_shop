from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_http_methods, require_POST
from basket.forms import AddToBasketForm
from shipping.forms import ShippingAddressForm
from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from basket.models import Basket, BasketLine, BasketCheckout
from basket.serializers import BasketLineListAddSerializer, BasketListSerializer, BasketCheckoutSerializer
from finance.models import Gateway, Payment


class BasketLineDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BasketLineListAddSerializer
    queryset = BasketLine.objects.all()

    def get_queryset(self):
        qs = super(BasketLineDeleteAPIView, self).get_queryset()
        basket_id = self.request.COOKIES.get('basket_id', None)
        basket = Basket.get_basket(basket_id)
        if not basket.check_authenticate(self.request.user):
            raise Http404
        return qs.filter(basket__id=basket.id)

    def perform_update(self, serializer):
        basket_id = self.request.COOKIES.get('basket_id', None)
        basket = Basket.get_basket(basket_id)
        if not basket.check_authenticate(self.request.user):
            raise Http404
        serializer.save(basket=basket)


class BasketListAddAPIView(ListCreateAPIView):
    serializer_class = BasketListSerializer
    queryset = Basket.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BasketListSerializer
        return BasketLineListAddSerializer

    def perform_create(self, serializer):
        basket_id = self.request.COOKIES.get('basket_id', None)
        basket = Basket.get_basket(basket_id)
        if not basket.check_authenticate(self.request.user):
            raise Http404
        serializer.save(basket=basket)

    def get_queryset(self):
        qs = super(BasketListAddAPIView, self).get_queryset()
        basket_id = self.request.COOKIES.get('basket_id', None)
        basket = Basket.get_basket(basket_id)
        if not basket.check_authenticate(self.request.user):
            raise Http404
        return qs.filter(id=basket.id)

    def list(self, request, *args, **kwargs):
        response = super(BasketListAddAPIView, self).list(request, *args, **kwargs)
        basket_id = request.COOKIES.get('basket_id', None)
        basket = Basket.get_basket(basket_id)
        if basket is None:
            raise Http404

        response.set_cookie('basket_id', basket.id)

        if not basket.check_authenticate(request.user):
            raise Http404
        return response


class BasketCheckoutListAddAPIView(ListCreateAPIView):
    serializer_class = BasketCheckoutSerializer
    queryset = BasketCheckout.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(BasketCheckoutListAddAPIView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        link = instance.payment.bank_page
        data = dict(link=link)
        return Response(data=data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        basket_id = self.request.COOKIES.get('basket_id', None)
        if basket_id is None:
            raise Http404
        basket = Basket.get_basket(basket_id)
        return serializer.save(user=self.request.user, basket=basket)


class VerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):

        authority = request.GET.get('Authority')
        try:
            payment = Payment.objects.get(authority=authority)
        except Payment.DoseNotExsit:
            return Http404

        data = dict(merchant_id=payment.gateway.auth_data, amount=payment.amount, authority=authority)

        paid = payment.verify(data)
        if paid:
            data = dict(status='پرداخت موفقیت امیز')
        else:
            data = dict(status='پرداخت ناموفق')
        response = Response(data=data)
        if paid:
            response.set_cookie('basket_id', None)
        return response


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


class VerifyView(View):
    template_name = "basket/cart.html"

    def get(self, request, *args, **kwargs):
        response = render(request, self.template_name)
        authority = request.GET.get('Authority')
        try:
            payment = Payment.objects.get(authority=authority)
        except Payment.DoseNotExsit:
            return Http404

        data = dict(merchant_id=payment.gateway.auth_data, amount=payment.amount, authority=authority)

        paid = payment.verify(data)
        if paid:
            response.set_cookie('basket_id', None)
        return response















