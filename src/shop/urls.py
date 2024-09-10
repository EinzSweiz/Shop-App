"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import urls as main_urls
from goods import urls as goods_urls
from users import urls as users_urls
from cards import urls as cards_urls
from orders import urls as orders_urls
from django.conf import settings
from main.views import custom_404_view
from django.conf.urls.static import static
DEBUG = getattr(settings, 'DEBUG')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(main_urls)),
    path('catalog/', include(goods_urls)),
    path('user/', include(users_urls)),
    path('bascket/', include(cards_urls)),
    path('orders/', include(orders_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

handler404 = custom_404_view