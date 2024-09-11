from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from cards.models import Card
from orders.forms import OrderForm
from django.shortcuts import redirect
from orders.models import Order, OrderItem
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = OrderForm
    success_url = reverse_lazy('users:profile')

    def get_initial(self):
        initinal = super().get_initial()
        initinal['first_name'] = self.request.user.first_name
        initinal['last_name'] = self.request.user.last_name
        return initinal 
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
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
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save()
                    cart_items.delete()
                    messages.success(self.request, 'Order Done')
                    return redirect(self.success_url)
        except Exception as e:
            messages.success(self.request, str(e))
            return redirect(reverse_lazy('orders:create_order'))
        
    def form_invalid(self, form):
        messages.error(self.request, 'Error happened')
        return redirect('orders:create_order')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Create Order'
        return context
# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     cart_items = Card.objects.filter(user=user)
#                     if cart_items.exists():
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number = form.cleaned_data['phone_number'],
#                             requires_delivery = form.cleaned_data['requires_delivery'],
#                             delivery_address = form.cleaned_data['delivery_address'],
#                             payment_on_get = form.cleaned_data['payment_on_get'],
#                         )
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             price = cart_item.product.total_price()
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise ValidationError(f'Not enough product {name} in store\
#                                                       in stock {quantity}')
                            
#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity
#                             )
#                             product.quantity -= quantity
#                             product.save()
#                         cart_items.delete()
#                         messages.success(request, 'Order Done!')
#                         return redirect('users:profile')
#             except Exception as e:
#                 messages.success(request, str(e))
#                 return redirect('orders:create_order')

#     else:
#         initial = {
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name,
#         }
#         form = OrderForm(initial=initial)
#     context = {
#         'title': 'Place-an-order',
#         'form': form
#     }
#     return render(request, 'orders/create_order.html', context)