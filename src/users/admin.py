from django.contrib import admin
from cards.admin import CardTabAdmin
from users.models import User
from orders.admin import OrdersTabularAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'image']
    search_fields = ['first_name', 'last_name', 'username', 'email']

    inlines = [CardTabAdmin, OrdersTabularAdmin]

