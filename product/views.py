from django.db.models import Count
from django.shortcuts import render, redirect

from basket.forms import AddToBasketForm
from comment.forms import CommentForm
from comment.models import Comment
from product.forms import ProductRateForm
from product.models import Product, ProductView, ProductRate


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
            product_view1 = ProductView.objects.filter(product=product).aggregate(view_product=Count('ip'))
            product_view2 = product_view1.get('view_product')
            comments = Comment.objects.filter(reply=None, product=product)
            form_comment = CommentForm({'product': product})
            form = AddToBasketForm({'product': product, 'quantity': 1})
            form_rate = ProductRateForm({'product': product, 'rate': 1})
            rate = ProductRate.avg(product)
            context = {'product': product, "form": form, 'form_comment': form_comment, 'comments': comments,
                       'rate': rate, 'form_rate': form_rate, 'view': product_view2}
            return render(request, 'products/product_details.html', context=context)


def rate_view(request, product_slug):
    form = ProductRateForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        form.save()
    return redirect('product-detail', product_slug)






