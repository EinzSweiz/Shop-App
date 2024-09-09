from django.db import models
from users.models import User
from goods.models import Products

class CardQueryset(models.QuerySet):

    def final_price(self):
        return sum(card.products_price() for card in self)
    
    def total_count(self):
        if self:
            return sum(card.quantity for card in self)
        return 0

class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'card'
        verbose_name = 'Bascket'
        verbose_name_plural = 'Basckets'

    objects = CardQueryset.as_manager()

    def products_price(self):
        return round(self.product.total_price() * self.quantity, 2)

    def __str__(self) -> str:
        return f'Backet {self.user} | Product {self.product} | Quantity {self.quantity}'