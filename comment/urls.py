from django.urls import path

from comment.views import CommentListPostAPIView, CommentUpdateAPIView

urlpatterns = [
    path('list/<slug:slug_product>/', CommentListPostAPIView.as_view(), name='list-comment'),
    path('list/<slug:slug_product>/<int:comment_id>/', CommentListPostAPIView.as_view(), name='reply-comment'),
    path('edit/<int:pk>/', CommentUpdateAPIView.as_view(), name='edit-comment')


]