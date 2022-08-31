from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from category.models import Category
from product.models import ProductImage, Product


class CreateImageSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product')


class CreateListProductSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True)
    modified_time = serializers.DateTimeField(read_only=True)
    sale_number = serializers.IntegerField(read_only=True, default=0)
    images = serializers.SerializerMethodField()
    category = serializers.SlugField(source='category.slug')

    class Meta:
        model = Product
        fields = ('type', 'name', 'category', 'amount', 'description', 'price', 'sale_number',
                  'slug', 'create_time', 'modified_time', 'images')

    def get_images(self, obj):
        images = obj.images.all()
        serializer = CreateImageSerializer(images, many=True)
        return serializer.data

    def create(self, validated_data):
        instance = get_object_or_404(Category, slug=validated_data['category']['slug'])
        validated_data['category'] = instance
        cr = super().create(validated_data)
        return cr

