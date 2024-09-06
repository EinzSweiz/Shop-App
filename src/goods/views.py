from django.shortcuts import render, get_object_or_404
from goods.models import Products


def catalog(request):
    goods = Products.objects.all()
    context = {
        'title': 'Home-Catalog',
        'goods': goods
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)
    return render(request, 'goods/product.html', {"product": product})
