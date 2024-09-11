from django.urls import path
from users import views

app_name = "users" 

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name="login"),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('users-cards/', views.UserCardView.as_view(), name='users-cards'),
    path('profile/', views.ProfileUserView.as_view(), name='profile')
]