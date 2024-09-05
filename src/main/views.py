from django.shortcuts import render


def index(request):
    context = {
        'title': 'Home - Main',
        'content': 'Магазин мебели HOME',
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'About-us',
        'content': 'About Us'
    }
    return render(request, 'main/about.html', context)
