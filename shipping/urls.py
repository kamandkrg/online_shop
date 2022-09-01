from django.urls import path

from shipping.views import ShippingAddressAddListAPIView, DestroyUpdateShippingAddressAPIView

urlpatterns = [
    path('api/list/', ShippingAddressAddListAPIView.as_view(), name='shipping-list-add'),
    path('api/edit/<int:pk>/', DestroyUpdateShippingAddressAPIView.as_view(), name='shipping-edit')
]

