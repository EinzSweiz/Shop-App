from django.db import models

from goods.models import Products
from users.models import User



class OrderItemQueryset(models.QuerySet):
    def total_price(self):
        return sum(card.products_price() for card in self)
    
    def total_quantity(self):
        if self:
            return sum(card.quantity for card in self)
        return 0
    


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    requires_delivery = models.BooleanField(default=False)
    delivery_address = models.TextField(blank=True, null=True) 
    payment_on_get = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='In processing')  

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self) -> str:
        return  f"Order No {self.pk} | Buyer {self.user.first_name} {self.user.last_name}"



class OrderTime(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, default=None)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Sold Item'
        verbose_name_plural = 'Sold Items'

    objects = OrderItemQueryset.as_manager()

    def products_price(self):
        return round(self.product.price * self.product.quantity, 2)
    
    def __str__(self) -> str:
        return f'Product {self.name} | Order {self.order.pk}'