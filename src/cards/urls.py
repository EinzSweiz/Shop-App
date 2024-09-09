from django.urls import path
from cards import views
app_name = 'cards'

urlpatterns = [
    path('add_product/<slug:product_slug>', views.bascket_add, name='add_product'),
    path('change_product/<slug:product_slug>', views.bascket_change, name='change_product'),
    path('remove_product/<slug:product_slug>', views.bascket_remove, name='remove_product'),

]   