
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib import messages

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)  # Pass request and data for authentication
        if form.is_valid():
            username = form.cleaned_data['username']  # Access cleaned data
            password = form.cleaned_data['password']  # Access cleaned data
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'You are logged in')
                return redirect('main:home')
            else:
                # Add a non-field error if authentication fails
                form.add_error(None, 'Invalid username or password')
        else:
            # Add a non-field error if form submission is invalid
            form.add_error(None, 'Invalid form submission')
    else:
        form = UserLoginForm()

    context = {
        'title': 'Login User',
        'form': form,
    }
    return render(request, 'users/login.html', context)

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('main:home')
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Login User',
        'form': form
    }
    return render(request, 'users/registration.html', context)

def logout_user(request):
    logout(request)
    return redirect('main:home')
    

def profile_user(request):
    context = {
        'title': 'Profile User'
    }
    return render(request, 'users/profile.html', context)