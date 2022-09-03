from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from category.models import Category
from product.models import ProductImage, Product, ProductRate


class CreateImageSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product')


class ProductRateSerializer(serializers.ModelSerializer):
    product = serializers.SlugField(source='product.slug', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    avg = serializers.SerializerMethodField()

    class Meta:
        model = ProductRate
        fields = ('product', 'user', 'rate', 'avg')

    def get_avg(self, obj):
        return obj.avg(obj.product)


class CreateListProductSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    modified_time = serializers.DateTimeField(read_only=True)
    sale_number = serializers.IntegerField(read_only=True, default=0)
    images = serializers.SerializerMethodField(read_only=True)
    category = serializers.SlugField(source='category.slug', allow_blank=True)

    class Meta:
        model = Product
        fields = ('type', 'name', 'category', 'amount', 'description', 'price', 'sale_number',
                  'slug', 'create_time', 'modified_time', 'images')

    def get_images(self, obj):
        images = obj.images.all()
        serializer = CreateImageSerializer(images, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        validated_data['category'] = get_object_or_404(Category, slug=validated_data['category']['slug'])

        cr = super().update(instance, validated_data)
        return cr


