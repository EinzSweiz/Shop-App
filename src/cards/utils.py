
from cards.models import Card


def get_user_cards(request):
    if request.user.is_authenticated:
        return Card.objects.filter(user=request.user)

    if not request.session.session_key:
        request.session.create()
    return Card.objects.filter(session_key=request.session.session_key)