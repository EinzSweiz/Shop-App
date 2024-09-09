from django.shortcuts import render, redirect
from cards.utils import get_user_cards
from goods.models import Products
from .models import Card
from django.http import JsonResponse
from django.template.loader import render_to_string

def bascket_add(request):
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)
    if request.user.is_authenticated:
        cards = Card.objects.filter(user=request.user, product=product)
        if cards.exists():
            card =  cards.first()
            if card:
                card.quantity += 1
                card.save()
        else:
            Card.objects.create(user=request.user, product=product, quantity=1)
    
    user_card = get_user_cards(request)
    card_items_html =  render_to_string(
        'includes/included_card.html', {'cards': user_card}, request=request
    )
    response_data = {
        'message': 'Product added',
        'cart_items_html': card_items_html
    }
    return JsonResponse(response_data)

def bascket_change(request):
    pass
#     product = Products.objects.get(slug=product_slug)
#     if request.user.is_authenticated:
#         card = Card.objects.filter(user=request.user, product=product).first()
#         if card and card.quantity > 0:
#             card.quantity -= 1
#             card.save()
#         elif card and card.quantity == 0:
#             card.delete()
#     referer = request.META.get('HTTP_REFERER', 'main:home')
#     return redirect(referer)

def bascket_remove(request):
    cart_id = request.POST.get('cart_id')
    card = Card.objects.get(id=cart_id)
    quantity = card.quantity
    card.delete()

    user_card = get_user_cards(request)
    cart_items_html = render_to_string(
        'includes/included_card.html',
        {'cards': user_card},
        request=request
    )
    response_data = {
        'message': 'Product removed',
        'cart_items_html': cart_items_html,
        'quantity_deleted': quantity
    }
    return JsonResponse(response_data)