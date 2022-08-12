from django.shortcuts import render
from django.views.decorators.http import require_POST

from comment.models import Comment


@require_POST
def send_comment(request):
    pass
