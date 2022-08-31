from django.urls import path

from category.views import show_detail

urlpatterns = [
    path('all/<slug:slug_category>/', show_detail, name='show-detail'),
    path('api/list-add/', CategoryListCreateAPIView.as_view(), name='list-add-category'),
    path('api/update/<slug:slug_category>/', CategoryUpdateAPIView.as_view(), name='update-category')
]








