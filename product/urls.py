from django.urls import path

from product.views import product_detail, product_list

urlpatterns = [
    path('list-product/', product_list),
    path('detail-product/<slug:product_slug>/', product_detail)

]
