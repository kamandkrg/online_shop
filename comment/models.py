from django.conf import settings
from django.db import models

from product.models import Product


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reply}/{self.user}"

    @classmethod
    def create(cls, text, user, reply=None):
        comment = cls.objects.create(text=text, user=user, reply=reply)
        return comment





