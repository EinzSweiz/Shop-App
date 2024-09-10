from django.contrib import admin
from orders.models import Order, OrderItem



class OrdersTabularAdmin(admin.TabularInline):
    model = Order
    fields = [
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid',
        'created_timestamp'
    ]
    search_fields = [
        'id',
        'payment_on_get',
        'is_paid',
        'created_timestamp',
    ]
    readonly_fields = ['created_timestamp']
    extra = 0
class OrderItemTabularAdmin(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'name', 'price', 'quantity']
    search_fields = ['product', 'name']
    extra = 0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid',
        'created_timestamp',

    ]
    readonly_fields = ('created_timestamp', )
    list_display_links = ['user']
    search_fields = [
        'id',
    ]
    list_filter = [
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid',
        'created_timestamp',

    ]
    inlines = (OrderItemTabularAdmin, )


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'name',
        'price',
        'quantity',
        'created_timestamp'
    ]

    search_fields = [
        'order',
        'product',
        'name'
    ]
