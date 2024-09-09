from django.urls import path
from cards import views
app_name = 'cards'

urlpatterns = [
    path('add_product/', views.bascket_add, name='add_product'),
    path('change_product/', views.bascket_change, name='change_product'),
    path('remove_product/', views.bascket_remove, name='remove_product'),

]   