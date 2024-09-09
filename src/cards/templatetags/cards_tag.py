from django import template
from cards.models import Card


register = template.Library()


@register.simple_tag()
def user_cards(request):
    return Card.objects.filter(user=request.user)