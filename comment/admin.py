from django.contrib import admin
from django.contrib.admin import register

from comment.models import Comment


@register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text']
