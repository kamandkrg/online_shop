from rest_framework import serializers

from comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    product = serializers.SlugField(source='product.slug', read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    modify_time = serializers.DateTimeField(read_only=True)
    children = serializers.SerializerMethodField()
    reply = serializers.IntegerField(source='reply.id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'product', 'reply', 'children', 'created_time', 'modify_time')

    def get_children(self, obj):
        children = obj.children.all()
        serializer = CommentListSerializer(children, many=True)
        return serializer.data

