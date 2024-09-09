from django.urls import path
from cards import views
app_name = 'cards'

urlpatterns = [
    path('add/<int:product_id>', views.backet_add, name='add'),
    path('change/<int:product_id>', views.backet_change, name='change'),
    path('remove/<int:product_id>', views.backet_remove, name='remove'),

]