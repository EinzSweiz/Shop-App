
from cards.models import Card


def get_user_cards(request):
    if request.user.is_authenticated:
        return Card.objects.filter(user=request.user)