from django.forms import ValidationError
from django.shortcuts import render
from django.contrib import messages
from cards.models import Card
from orders.forms import OrderForm
from django.shortcuts import redirect
from orders.models import Order, OrderItem
from django.db import transaction
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
                    cart_items = Card.objects.filter(user=user)
                    if cart_items.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number = form.cleaned_data['phone_number'],
                            requires_delivery = form.cleaned_data['requires_delivery'],
                            delivery_address = form.cleaned_data['delivery_address'],
                            payment_on_get = form.cleaned_data['payment_on_get'],
                        )
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.total_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Not enough product {name} in store\
                                                      in stock {quantity}')
                            
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity
                            )
                            product.quantity -= quantity
                            product.save()
                        cart_items.delete()
                        messages.success(request, 'Order Done!')
                        return redirect('users:profile')
            except Exception as e:
                messages.success(request, str(e))
                return redirect('orders:create_order')

    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = OrderForm(initial=initial)
    context = {
        'title': 'Place-an-order',
        'form': form
    }
    return render(request, 'orders/create_order.html', context)