from django.urls import path, include
from . import views
from django.views.decorators.cache import cache_page
app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('about/', cache_page(60*5)(views.AboutView.as_view()), name='about')
]