from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Products, Categories
from django.core.paginator import Paginator


def catalog(request, category_slug):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    if category_slug == 'all-products':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products, category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)
    
    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)
    
    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    context = {
        'title': 'Home-Catalog',
        'goods': current_page,
        'slug_url': category_slug,
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    return render(request, 'goods/product.html', {"product": product})
