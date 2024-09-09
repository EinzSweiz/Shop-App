from django.db import models
from users.models import User
from goods.models import Products

class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bascket'
        verbose_name_plural = 'Basckets'

    def __str__(self) -> str:
        return f'Backet {self.user} | Product {self.product} | Quantity {self.quantity}'