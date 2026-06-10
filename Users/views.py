from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect

from .forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("blog:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, f"Welcome, {self.object.first_name or self.object.username}!")
        return response


class SVLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirect to blog list after successful login"""
        return reverse_lazy("blog:list")

    def form_valid(self, form):
        """Add success message on login"""
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {self.request.user.first_name or self.request.user.username}!")
        return response


class SVLogoutView(LogoutView):
    next_page = "blog:list"

    def dispatch(self, request, *args, **kwargs):
        """Add logout message"""
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, "You have been successfully logged out.")
        return response