from django.shortcuts import render, redirect

from basket.forms import AddToBasketForm
from comment.forms import CommentForm
from comment.models import Comment
from product.models import Product, ProductView


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
            comments = Comment.objects.filter(reply=None)
            form_comment = CommentForm({'product': product})
            form = AddToBasketForm({'product': product, 'quantity': 1})
            context = {'product': product, "form": form, 'form_comment': form_comment, 'comments': comments}
            return render(request, 'products/product_details.html', context=context)








