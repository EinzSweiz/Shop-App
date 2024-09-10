from django.contrib import admin
from cards.models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['user', "product_name", 'quantity', 'created_timestamp']
    list_filter = ['created_timestamp', 'user', 'product__name']

    def product_name(self, obj):
        return str(obj.product.name )
class CardTabAdmin(admin.TabularInline):
    model = Card
    fields = 'product', 'quantity', 'created_timestamp'
    search_fields = 'product', 'quantity', 'created_timestamp'
    readonly_fields = ('created_timestamp', )
    extra = 1 
