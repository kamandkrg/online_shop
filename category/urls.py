from django.urls import path

from category.views import show_all, show_detail

urlpatterns = [
    path('show-all/', show_all, name='show-all'),
    path('all/<slug:slug_category>/', show_detail, name='show-detail'),
]








