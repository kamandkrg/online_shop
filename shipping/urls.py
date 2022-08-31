from django.urls import path

from shipping.views import ShippingAddressAddListAPIView

urlpatterns = [
    path('list/', ShippingAddressAddListAPIView.as_view(), name='shipping-list-add')
]

