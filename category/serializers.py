from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SlugField(allow_null=True, allow_blank=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'parent', 'slug', 'children')

    def get_children(self, obj):
        children = obj.children.all()
        serializer = CategorySerializer(children, many=True)
        return serializer.data

    def create(self, validated_data):
        if validated_data['parent']:
            parent = get_object_or_404(Category, slug=validated_data['parent'])
            validated_data['parent'] = parent
        else:
            validated_data['parent'] = None
        cr = super().create(validated_data)
        return cr

    def update(self, instance, validated_data):
        if validated_data['parent']:
            parent = get_object_or_404(Category, slug=validated_data['parent'])
            validated_data['parent'] = parent
        else:
            validated_data['parent'] = None
        cr = super().update(instance, validated_data)
        return cr


