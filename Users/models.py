# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class Role(models.TextChoices):
    SEEKER = 'seeker', 'Seeker'
    EMPLOYEE = 'employee', 'Employee'

class User(AbstractUser):
    # Remove username if you want email as login (optional)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.SEEKER
    )
    
    # Override the groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Profile(models.Model):
    """Main profile information"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        null=True,
        blank=True
    )
    
    # Personal Information
    name = models.CharField(max_length=200, default='John Doe')
    title = models.CharField(max_length=200, default='Web Developer')
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)
    about_text = models.TextField()
    
    # Contact Information
    phone = models.CharField(max_length=20, default='+012 345 6789')
    email = models.EmailField(default='info@example.com')
    address = models.CharField(max_length=500, default='123 Street, New York, USA')
    
    # Professional Details
    birthday = models.DateField(null=True, blank=True)
    degree = models.CharField(max_length=100, default='Master')
    experience_years = models.IntegerField(default=10)
    freelance_status = models.CharField(
        max_length=50,
        choices=[('available', 'Available'), ('unavailable', 'Unavailable')],
        default='available'
    )
    
    # Statistics
    years_of_experience = models.IntegerField(default=10)
    happy_clients = models.IntegerField(default=100)
    completed_projects = models.IntegerField(default=200)
    
    # Social Links
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    
    # Typed Text (comma-separated values)
    typed_texts = models.TextField(
        help_text="Enter comma-separated values like: Web Designer, Web Developer, Front End Developer",
        default='Web Designer, Web Developer, Front End Developer, Apps Designer, Apps Developer'
    )
    
    # CV Download
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_typed_list(self):
        return [text.strip() for text in self.typed_texts.split(',')]
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

class Skill(models.Model):
    """Skills with progress percentage"""
    SKILL_COLORS = [
        ('primary', 'Primary (Blue)'),
        ('success', 'Success (Green)'),
        ('info', 'Info (Cyan)'),
        ('warning', 'Warning (Yellow)'),
        ('danger', 'Danger (Red)'),
        ('secondary', 'Secondary (Gray)'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    percentage = models.IntegerField(help_text="Percentage from 0 to 100")
    color = models.CharField(max_length=20, choices=SKILL_COLORS, default='primary')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.percentage}%"

class Experience(models.Model):
    """Work experience entries"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-order', '-start_date']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    def get_date_range(self):
        start = self.start_date.strftime('%Y')
        end = 'Present' if self.is_current else self.end_date.strftime('%Y')
        return f"{start} - {end}"

class Education(models.Model):
    """Education entries"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-order', '-end_year']
    
    def __str__(self):
        return f"{self.degree} from {self.institution}"

class Service(models.Model):
    """Services offered"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='services')
    icon = models.CharField(
        max_length=50,
        help_text="Font Awesome icon class (e.g., fa-laptop-code, fa-android, fa-search, fa-edit)",
        default='fa-laptop-code'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class PortfolioCategory(models.Model):
    """Categories for portfolio items"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    filter_class = models.CharField(max_length=50, help_text="CSS class for filtering (e.g., first, second)")
    
    def __str__(self):
        return self.name

class PortfolioItem(models.Model):
    """Portfolio/Gallery items"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(PortfolioCategory, on_delete=models.SET_NULL, null=True, related_name='items')
    image = models.ImageField(upload_to='portfolio/')
    description = models.TextField(blank=True)
    project_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """Client testimonials"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='testimonials')
    client_name = models.CharField(max_length=200)
    client_profession = models.CharField(max_length=200)
    client_image = models.ImageField(upload_to='testimonials/', default='testimonials/default.jpg', blank=True, null=True)
    testimonial_text = models.TextField()
    rating = models.IntegerField(default=5, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', '-id']
    
    def __str__(self):
        return f"Testimonial by {self.client_name}"

class NewsletterSubscriber(models.Model):
    """Newsletter subscribers"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    """Contact form messages"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='contact_messages', null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name}: {self.subject}"
    
    class Meta:
        ordering = ['-created_at']

class SiteSetting(models.Model):
    """Global site settings"""
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='site_settings')
    site_name = models.CharField(max_length=200, default='DarkCV')
    footer_text = models.CharField(max_length=500, default='All Rights Reserved. Designed by HTML Codex')
    show_subscribe_section = models.BooleanField(default=True)
    subscribe_title = models.CharField(max_length=200, default='Subscribe My Newsletter')
    subscribe_text = models.CharField(max_length=500, default='Subscribe and get my latest article in your inbox')
    contact_form_active = models.BooleanField(default=False)
    contact_form_message = models.TextField(
        default='The contact form is currently inactive. Contact form functionality coming soon.',
        help_text="Message shown when contact form is inactive"
    )
    
    def __str__(self):
        return f"Settings for {self.profile.name}"