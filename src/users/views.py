from django.shortcuts import render
from django.contrib.auth import logout



def login_user(request):
    context = {
        'title': 'Login User'
    }
    return render(request, 'users/login.html', context)


def register_user(request):
    context = {
        'title': 'Login User'
    }
    return render(request, 'users/registration.html', context)

def logout_user(request):
    logout(request)
    

def profile_user(request):
    context = {
        'title': 'Profile User'
    }
    return render(request, 'users/profile.html', context)