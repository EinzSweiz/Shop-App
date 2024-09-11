from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView



class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Main'
        context['content'] = 'Shop of Furniture - Home'
        return context



class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['title'] = 'About-us'
        context['content'] = 'This site was created by DarkKnight'
        return context


def custom_404_view(request, exception):
    return render(request, '404error.html')
