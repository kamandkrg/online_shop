from django.http import Http404
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from basket.models import Basket, BasketLine, BasketCheckout
from finance.models import Gateway
from product.models import Product
from shipping.models import ShippingAddress
from shipping.seializers import ShippingAddressSerializer


class BasketLineListAddSerializer(serializers.ModelSerializer):
    basket = serializers.IntegerField(source='basket.id', read_only=True)
    product = serializers.SlugField(source='product.slug')
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = BasketLine
        fields = ('id', 'basket', 'product', 'quantity')

    def save(self, **kwargs):
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )
        validated_data = {**self.validated_data, **kwargs}
        if self.instance is not None:
            validated_data['product'] = get_object_or_404(Product, slug=validated_data['product']['slug'])
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
            return self.instance
        else:
            basket = validated_data['basket']
            product = get_object_or_404(Product, slug=validated_data['product']['slug'])
            quantity = validated_data['quantity']
            line = basket.add(product, quantity)
            return line


class BasketListSerializer(serializers.ModelSerializer):
    lines = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'created_time', 'modify_time', 'user', 'lines')

    def get_lines(self, obj):
        lines = obj.lines.all()
        serializer = BasketLineListAddSerializer(lines, many=True)
        return serializer.data


class BasketCheckoutSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    payment = serializers.UUIDField(source='payment.invoice_number', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    basket = serializers.IntegerField(source='basket.id', read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    address_id = serializers.IntegerField(source='address.id', allow_null=True)
    payment_gateway_id = serializers.IntegerField(source='payment.gateway.id', allow_null=True)

    class Meta:
        model = BasketCheckout
        fields = ('status', 'basket', 'user', 'payment', 'address_id', 'address', 'total_price', 'payment_gateway_id')

    def get_address(self, obj):
        address = obj.address
        serializer = ShippingAddressSerializer(address)
        return serializer.data

    def get_status(self, obj):
        return obj.get_status_display()

    def create(self, validated_data):
        address = ShippingAddress.objects.filter(user=validated_data['user'], id=validated_data['address']['id'])
        if not address.exists():
            raise Http404
        basket_checkout = BasketCheckout.create(validated_data['basket'], validated_data['user'], address.first())
        gateway = Gateway.objects.get(pk=validated_data['payment']['gateway']['id'])
        basket_checkout.payment.gateway = gateway
        return basket_checkout

