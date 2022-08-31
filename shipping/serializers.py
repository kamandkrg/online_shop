from rest_framework import serializers

from shipping.models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShippingAddress
        fields = ('id', 'user', 'city', 'address', 'zipcode', 'number')


