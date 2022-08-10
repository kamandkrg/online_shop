from django.urls import path

from basket.views import add_to_basket, show_basket, delete_item

urlpatterns = [
    path('add/', add_to_basket, name='add-to-basket'),
    path('show/', show_basket, name='show-basket'),
    path('delete/<int:pk>', delete_item, name='delete-item'),
]