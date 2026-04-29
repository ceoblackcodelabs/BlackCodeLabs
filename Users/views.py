# Users/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

# Option 1: Using CreateView for registration
class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        messages.success(self.request, f'Account created successfully! Please login.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

# Option 2: Custom registration with auto-login
class UserRegistrationAutoLoginView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        # Auto-login after registration
        login(self.request, user)
        messages.success(self.request, f'Welcome {user.first_name}! You are now logged in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

# Using Django's built-in LoginView
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:profile')
    
    def get_success_url(self):
        return self.success_url
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back {form.get_user().first_name}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

# Custom login view without using built-in (alternative)
class CustomUserLoginView(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back {user.first_name}!')
                return redirect('users:profile')
        messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name, {'form': form})

# Logout View
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)

# Dashboard view (protected)
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        # Add role-specific context
        if self.request.user.role == 'seeker':
            context['message'] = 'Welcome Seeker! Find your opportunities here.'
        else:
            context['message'] = 'Welcome Employee! Manage your tasks here.'
        return context

# Profile view
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user's profile (assuming one profile exists)
        try:
            profile = Profile.objects.first()  # Get the first profile
            context['profile'] = profile
            
            # Get all related data
            context['skills'] = Skill.objects.filter(profile=profile).order_by('order')
            context['experiences'] = Experience.objects.filter(profile=profile).order_by('-order', '-start_date')
            context['educations'] = Education.objects.filter(profile=profile).order_by('-order', '-end_year')
            context['services'] = Service.objects.filter(profile=profile).order_by('order')
            context['portfolio_items'] = PortfolioItem.objects.filter(profile=profile).order_by('order')
            context['portfolio_categories'] = PortfolioCategory.objects.all()
            context['testimonials'] = Testimonial.objects.filter(profile=profile, is_active=True).order_by('order')
            context['site_settings'] = SiteSetting.objects.filter(profile=profile).first()
        except Profile.DoesNotExist:
            context['profile'] = None
            context['skills'] = []
            context['experiences'] = []
            context['educations'] = []
            context['services'] = []
            context['portfolio_items'] = []
            context['portfolio_categories'] = []
            context['testimonials'] = []
            context['site_settings'] = None
        
        context['user'] = self.request.user
        return context
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import NewsletterSubscriber, ContactMessage, Profile

@require_http_methods(["POST"])
def subscribe_newsletter(request):
    email = request.POST.get('email')
    if email:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            return JsonResponse({'message': 'Successfully subscribed to newsletter!'})
        else:
            return JsonResponse({'error': 'Email already subscribed.'}, status=400)
    return JsonResponse({'error': 'Invalid email address.'}, status=400)

@require_http_methods(["POST"])
def send_contact_message(request):
    profile = Profile.objects.first()
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    
    if name and email and subject and message:
        ContactMessage.objects.create(
            profile=profile,
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        return JsonResponse({'message': 'Message sent successfully! I\'ll get back to you soon.'})
    return JsonResponse({'error': 'Please fill in all fields.'}, status=400)