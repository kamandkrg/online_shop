from django.db.models import Q
from django.shortcuts import render

from product.models import Product
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from category.models import Category
from category.serializers import CategorySerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent=None)
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]


class CategoryUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'slug_category'
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]


def show_detail(request, slug_category):
    context = dict()
    category = Category.objects.get(slug=slug_category)
    products = Product.objects.filter(Q(category=category) | Q(category__parent=category))
    context['products'] = products
    return render(request, 'products/product_category.html', context=context)


