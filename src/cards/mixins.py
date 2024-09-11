from django.urls import reverse
from cards.models import Card
from cards.utils import get_user_cards
from django.template.loader import render_to_string

class CardMixin:
    def get_card(self, request, product=None, cart_id=None):
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            query_kwargs = {'session_key': request.session.session_key}
        
        if product:
            query_kwargs['product'] = product
        if cart_id:
            query_kwargs['id'] = cart_id
        
        return Card.objects.filter(**query_kwargs).first()
    
    def render_card(self, request):
        user_cart = get_user_cards(request)
        context = {'cards': user_cart}

        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context['order'] = True
        
        return render_to_string(
                'includes/included_card.html', context, request=request
        )