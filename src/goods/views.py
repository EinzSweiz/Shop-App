from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import Http404
from .models import Products, Categories
from goods.utils import q_search
from django.views.generic import DetailView, ListView

class CatalogView(ListView):
    model = Products
    # queryset = Products.objects.filter() --Can be done like this if needed
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 3
    allow_empty = False

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home-Catalog'
        context['slug_url'] = self.kwargs.get('category_slug')
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        if category_slug == 'all-products':
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()
        if on_sale:
            goods = goods.filter(discount__gt=0)
        
        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)
        
        return goods

class ProductView(DetailView):
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title']  = self.object.name
        return context 
    





# def catalog(request, category_slug=None):
#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)
#     if category_slug == 'all-products':
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = get_list_or_404(Products, category__slug=category_slug)

#     if on_sale:
#         goods = goods.filter(discount__gt=0)
    
#     if order_by and order_by != 'default':
#         goods = goods.order_by(order_by)
    
#     paginator = Paginator(goods, 3)
#     current_page = paginator.page(int(page))
#     context = {
#         'title': 'Home-Catalog',
#         'goods': current_page,
#         'slug_url': category_slug,
#     }
#     return render(request, 'goods/catalog.html', context)
