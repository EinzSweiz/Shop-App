from django.urls import path
from cards import views
app_name = 'cards'

urlpatterns = [
    path('add_product/', views.BascketAddView.as_view(), name='add_product'),
    path('change_product/', views.BascketChangeView.as_view(), name='change_product'),
    path('remove_product/', views.BascketRemoveView.as_view(), name='remove_product'),

]   