from django.urls import path

from product.views import product_detail, rate_view, ProductListAPIView, ProductUpdateDestroyAPIView, \
    ImageListCreateAPIView, ImageRetrieveDestroy, ProductCategoryCreateList

urlpatterns = [
    path('product-detail/<slug:product_slug>/', product_detail, name='product-detail'),
    path('create-rate/<slug:product_slug>/', rate_view, name='create-rate'),
    path('api/list/', ProductListAPIView.as_view(), name='list-product'),
    path('api/detail/<slug:slug_product>/', ProductUpdateDestroyAPIView.as_view(), name='detail-product'),
    path('api/images/<int:pk>/', ImageListCreateAPIView.as_view(), name='images-post'),
    path('api/images/<int:pk_product>/<int:pk>/', ImageRetrieveDestroy.as_view(), name='image-detail'),
    path('api/category/<slug:slug_category>/', ProductCategoryCreateList.as_view(), name='product-category'),


]
