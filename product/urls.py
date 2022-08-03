from django.urls import path

from product.views import product_detail

urlpatterns = [
    path('product-detail/<slug:product_slug>/', product_detail, name='product-detail')

]
