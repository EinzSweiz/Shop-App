from django.shortcuts import render, redirect
from goods.models import Products
from .models import Card

def bascket_add(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        cards = Card.objects.filter(user=request.user, product=product)
        if cards.exists():
            card =  cards.first()
            if card:
                card.quantity += 1
                card.save()
        else:
            Card.objects.create(user=request.user, product=product, quantity=1)
    referer = request.META.get('HTTP_REFERER', 'main:home')
    return redirect(referer)

def bascket_change(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        card = Card.objects.filter(user=request.user, product=product).first()
        if card and card.quantity > 0:
            card.quantity -= 1
            card.save()
        elif card and card.quantity == 0:
            card.delete()
    referer = request.META.get('HTTP_REFERER', 'main:home')
    return redirect(referer)

def bascket_remove(request, card_id):
    card = Card.objects.get(id=card_id)
    card.delete()
    referer = request.META.get('HTTP_REFERER', 'main:home')
    return redirect(referer)