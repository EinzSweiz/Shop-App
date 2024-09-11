from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.db.models import Prefetch
from cards.models import Card
from orders.models import Order, OrderItem
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
class LoginUserView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        session_key = self.request.session.session_key

        user = form.get_user()

        if user:
            login(self.request, user)
            if session_key:
                forgot_card = Card.objects.filter(user=user)
                if forgot_card.exists():
                    forgot_card.delete()
                Card.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f'{user.username}, You are logged in')
                return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.POST.get('next', None)
        if next_url and next_url != reverse_lazy('users:logout'):
            return next_url
        return reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class RegisterUserView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:profile')
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        session_key = self.request.session.session_key
        user = form.instance
      
        if user:
            form.save()
            login(self.request, user)
            if session_key:
                Card.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f'{user.username}, You are logged in')
                return redirect(self.success_url)
            

class ProfileUserView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, 'Profile successfully updated')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error happemed')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        orders = cache.get(f'orders_for_user_{self.request.user.id}')
        if not orders:
            context['orders'] = Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    'orderitem_set',
                    queryset=OrderItem.objects.select_related('product').order_by('-id')
                )
            )
            cache.set(f'orders_for_user_{self.request.user.id}', orders, 3600)
        context['orders'] = orders
        return context


class UserCardView(TemplateView):
    template_name = 'users/users-card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Bascket'
        return context



@login_required
def logout_user(request):
    messages.success(request, f'{request.user.username} you are successfully logged out ')
    logout(request)
    return redirect('main:home')


#NOTE Function versions 
# def login_user(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)  # Pass request and data for authentication
#         if form.is_valid():
#             username = form.cleaned_data['username']  # Access cleaned data
#             password = form.cleaned_data['password']  # Access cleaned data
#             user = authenticate(username=username, password=password)

#             session_key = request.session.session_key

#             if user:
#                 login(request, user)
#                 messages.success(request, f'{username} you are successfully logged in ')

#                 if session_key:
#                     Card.objects.filter(session_key=session_key).update(user=user)

#                 next_url = request.POST.get('next', None)
#                 if next_url and next_url != reverse('users:logout'):
#                     return redirect(next_url)    
#                 return redirect('main:home')
#             else:
#                 # Add a non-field error if authentication fails
#                 form.add_error(None, 'Invalid username or password')
#         else:
#             # Add a non-field error if form submission is invalid
#             form.add_error(None, 'Invalid form submission')
#     else:
#         form = UserLoginForm()

#     context = {
#         'title': 'Login User',
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)

# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()

#             session_key = request.session.session_key

#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 messages.success(request, f'{username} you are successfully registered ')
#                 if session_key:
#                     Card.objects.filter(session_key=session_key).update(user=user)
#                 return redirect('main:home')
#     else:
#         form = UserRegistrationForm()
#     context = {
#         'title': 'Register User',
#         'form': form
#     }
#     return render(request, 'users/registration.html', context)


# @login_required
# def profile_user(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully')
#             return redirect('users:profile')
#     else:
#         form = UserProfileForm(instance=request.user)
    
#     orders = Order.objects.filter(user=request.user).prefetch_related(
#         Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'))
#     ).order_by('-id')
    
#     context = {
#         'title': 'Profile User',
#         'form': form,
#         'orders': orders
#     }
#     return render(request, 'users/profile.html', context)


# def users_cards(request):
#     return render(request, 'users/users-card.html')
