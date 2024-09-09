from django.urls import path
from users import views

app_name = "users" 

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('users-cards/', views.users_cards, name='users-cards'),
    path('profile/', views.profile_user, name='profile')
]