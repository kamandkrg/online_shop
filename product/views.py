from django.db.models import Count
from django.shortcuts import render, redirect

from basket.forms import AddToBasketForm
from category.models import Category
from comment.forms import CommentForm
from comment.models import Comment
from product.forms import ProductRateForm
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, get_object_or_404, \
    RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from product.models import Product, ProductView, ProductRate, ProductImage
from product.serializers import CreateListProductSerializer, CreateImageSerializer, ProductRateSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateListProductSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]


class ProductUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, CreateAPIView):
    serializer_class = CreateListProductSerializer
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'slug_product'
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateImageSerializer
        return CreateListProductSerializer


class ProductCategoryCreateList(ListCreateAPIView):
    serializer_class = CreateListProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        qs = super().get_queryset()
        slug_category = self.kwargs['slug_category']
        return qs.filter(Q(category__slug=slug_category) | Q(category__parent__slug=slug_category))

    def perform_create(self, serializer):
        instance = get_object_or_404(Category, slug=self.kwargs['slug_category'])
        serializer.save(category=instance)


class ImageListCreateAPIView(ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = CreateImageSerializer
    permission_classes = (AllowAny, )

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(product__id=self.kwargs['pk'])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        serializer.save(product=product)


class ImageRetrieveDestroy(RetrieveDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = CreateImageSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser, )
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(product__id=self.kwargs['pk_product'])


class ProductRateCreateAPIView(ListCreateAPIView):
    serializer_class = ProductRateSerializer
    queryset = ProductRate.objects.all()

    def get_queryset(self):
        qs = super(ProductRateCreateAPIView, self).get_queryset()
        product = get_object_or_404(Product, slug=self.kwargs['slug_product'])
        return qs.filter(product=product)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, slug=self.kwargs['slug_product'])
        serializer.save(user=self.request.user, product=product)


def product_detail(request, product_slug):
    if request.method == 'POST':
        form_comment = CommentForm(request.POST)
        comment_id = request.POST.get('comment_id', None)

        if form_comment.is_valid():
            instance = form_comment.save(commit=False)
            instance.user = request.user
            if comment_id is not None:
                comment = Comment.objects.filter(pk=comment_id)
                if comment.exists():
                    instance.reply = comment.first()
            form_comment.save()
            return redirect('product-detail', product_slug)
    else:
        product = Product.objects.filter(slug=product_slug)
        if product.exists():
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ipaddress = x_forwarded_for.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')
            product = product.first()
            ProductView.increase_visit(product, ipaddress)
            product_view1 = ProductView.objects.filter(product=product).aggregate(view_product=Count('ip'))
            product_view2 = product_view1.get('view_product')
            comments = Comment.objects.filter(reply=None, product=product)
            form_comment = CommentForm({'product': product})
            form = AddToBasketForm({'product': product, 'quantity': 1})
            form_rate = ProductRateForm({'product': product, 'rate': 1})
            rate = ProductRate.avg(product)
            context = {'product': product, "form": form, 'form_comment': form_comment, 'comments': comments,
                       'rate': rate, 'form_rate': form_rate, 'view': product_view2}
            return render(request, 'products/product_details.html', context=context)


def rate_view(request, product_slug):
    form = ProductRateForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        form.save()
    return redirect('product-detail', product_slug)






