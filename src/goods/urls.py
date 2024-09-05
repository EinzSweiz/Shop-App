from django.urls import path, include
from . import views
app_name = 'goods'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('product/', views.product, name='product')
]