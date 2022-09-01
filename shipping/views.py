from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from shipping.models import ShippingAddress
from shipping.serializers import ShippingAddressSerializer


class ShippingAddressAddListAPIView(ListCreateAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super(ShippingAddressAddListAPIView, self).get_queryset()
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DestroyUpdateShippingAddressAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        qs = super(DestroyUpdateShippingAddressAPIView, self).get_queryset()
        return qs.filter(user=self.request.user)
