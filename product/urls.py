from django.urls import path

from product.views import product_detail, rate_view

urlpatterns = [
    path('product-detail/<slug:product_slug>/', product_detail, name='product-detail'),
    path('create-rate/<slug:product_slug>/', rate_view, name='create-rate'),

]
