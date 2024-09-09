from django import template
from cards.models import Card
from cards.utils import get_user_cards
     

register = template.Library()


@register.simple_tag()
def user_cards(request):
    return get_user_cards(request)