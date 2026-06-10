from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.SVLoginView.as_view(), name="login"),
    path("logout/", views.SVLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
