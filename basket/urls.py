from django.urls import path

from basket.views import add_to_basket, show_basket, delete_item, basket_checkout, VerifyView, BasketListAddAPIView, \
    BasketLineDeleteAPIView, BasketCheckoutListAddAPIView, VerifyViewAPIView

urlpatterns = [
    path('add/', add_to_basket, name='add-to-basket'),
    path('show/', show_basket, name='show-basket'),
    path('delete/<int:pk>', delete_item, name='delete-item'),
    path('checkout/', basket_checkout, name='checkout-basket'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('api/show-add/', BasketListAddAPIView.as_view(), name='list-add-basket'),
    path('api/detail-change/<int:pk>/', BasketLineDeleteAPIView.as_view(), name='change'),
    path('api/checkout/', BasketCheckoutListAddAPIView.as_view(), name='list-checkout'),
    path('api/verify/', VerifyViewAPIView.as_view(), name='verify')

]
