# Users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Registration URLs
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('register-auto/', views.UserRegistrationAutoLoginView.as_view(), name='register_auto'),

    path('login/', views.CustomUserLoginView.as_view(), name='custom_login'),
    
    # Logout URL
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('send-contact/', views.send_contact_message, name='send_contact'),
]