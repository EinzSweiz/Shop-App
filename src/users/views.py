from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.db.models import Prefetch
from cards.models import Card
from orders.models import Order, OrderItem
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)  # Pass request and data for authentication
        if form.is_valid():
            username = form.cleaned_data['username']  # Access cleaned data
            password = form.cleaned_data['password']  # Access cleaned data
            user = authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                login(request, user)
                messages.success(request, f'{username} you are successfully logged in ')

                if session_key:
                    Card.objects.filter(session_key=session_key).update(user=user)

                next_url = request.POST.get('next', None)
                if next_url and next_url != reverse('users:logout'):
                    return redirect(next_url)    
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

            session_key = request.session.session_key

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'{username} you are successfully registered ')
                if session_key:
                    Card.objects.filter(session_key=session_key).update(user=user)
                return redirect('main:home')
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Register User',
        'form': form
    }
    return render(request, 'users/registration.html', context)

@login_required
def logout_user(request):
    messages.success(request, f'{request.user.username} you are successfully logged out ')
    logout(request)
    return redirect('main:home')
    
@login_required
def profile_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'))
    ).order_by('-id')
    
    context = {
        'title': 'Profile User',
        'form': form,
        'orders': orders
    }
    return render(request, 'users/profile.html', context)


def users_cards(request):
    return render(request, 'users/users-card.html')

