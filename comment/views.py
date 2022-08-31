
from rest_framework.generics import ListCreateAPIView, get_object_or_404, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from comment.models import Comment
from comment.serializers import CommentListSerializer
from product.models import Product


class CommentListPostAPIView(ListCreateAPIView):
    queryset = Comment.objects.filter(reply=None)
    serializer_class = CommentListSerializer
    permission_classes = (AllowAny, )

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(product__slug=self.kwargs['slug_product'])

    def perform_create(self, serializer):
        if self.kwargs['comment_id']:
            comment = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        product = get_object_or_404(Product, slug=self.kwargs['slug_product'])
        serializer.save(user=self.request.user, product=product, reply=comment)


class CommentUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticated]

