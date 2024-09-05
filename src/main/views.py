from django.shortcuts import render
from django.http import HttpResponse
from goods.models import Categories


def index(request):
    categories = Categories.objects.all()
    context = {
        'title': 'Home - Main',
        'content': 'Магазин мебели HOME',
        'categories': categories,
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'About-us',
        'content': 'About Us'
    }
    return render(request, 'main/about.html', context)
