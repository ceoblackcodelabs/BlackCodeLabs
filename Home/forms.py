# Home/forms.py
from django import forms
from django.core.validators import RegexValidator
from .models import (
    ContactInquiry, DemoBooking, 
    CourseEnrollment, Course
)
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class ContactForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '+1 (555) 123-4567',
            'pattern': '^\+?1?\d{9,15}$'
        }),
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    
    # Add honeypot field for spam protection
    honeypot = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'display:none;'}),
        label='Leave this field empty'
    )
    
    class Meta:
        model = ContactInquiry
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'company', 'department', 'subject', 'message',
            'newsletter_subscribed'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
                'autocomplete': 'given-name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name',
                'autocomplete': 'family-name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com',
                'autocomplete': 'email'
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Your company name (optional)',
                'autocomplete': 'organization'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'How can we help you?'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Please provide details about your inquiry...',
                'rows': 6
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'newsletter_subscribed': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
    
    def clean_honeypot(self):
        """Check if honeypot field was filled (spam detection)"""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError("Spam detected.")
        return honeypot
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add any additional email validation here
        return email.lower()  # Store emails in lowercase
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        # Check for suspicious content
        spam_keywords = ['http://', 'https://', 'www.', '.com/', 'buy now', 'click here']
        if any(keyword in message.lower() for keyword in spam_keywords):
            # Could mark as potential spam or raise validation error
            pass
        return message
    
class DemoBookingForm(forms.ModelForm):
    # Hidden honeypot field for spam protection
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'honeypot'}),
        label='Leave this field empty'
    )
    
    class Meta:
        model = DemoBooking
        fields = [
            'first_name', 'last_name', 'email', 'company', 'job_title',
            'demo_date', 'demo_time', 'demo_title', 'service_type',
            'demo_message', 'terms_accepted', 'number_of_attendees'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your.email@company.com',
                'class': 'form-control'
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Your company name',
                'class': 'form-control'
            }),
            'job_title': forms.TextInput(attrs={
                'placeholder': 'Your position',
                'class': 'form-control'
            }),
            'demo_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            }),
            'demo_time': forms.Select(attrs={'class': 'form-control'}),
            'demo_title': forms.TextInput(attrs={
                'placeholder': 'E.g., Automation Solution Demo',
                'class': 'form-control'
            }),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'demo_message': forms.Textarea(attrs={
                'placeholder': 'Share any specific requirements or questions...',
                'rows': 5,
                'class': 'form-control'
            }),
            'number_of_attendees': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 50,
                'value': 1
            }),
            'terms_accepted': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set minimum date to tomorrow
        tomorrow = timezone.now() + timedelta(days=1)
        self.fields['demo_date'].widget.attrs['min'] = tomorrow.strftime('%Y-%m-%d')
    
    def clean_website(self):
        """Honeypot validation"""
        website = self.cleaned_data.get('website')
        if website:
            raise ValidationError("Spam detected.")
        return website
    
    def clean_demo_date(self):
        demo_date = self.cleaned_data.get('demo_date')
        
        if demo_date:
            # Ensure date is in the future
            today = timezone.now().date()
            if demo_date <= today:
                raise ValidationError("Please select a future date for the demo.")
            
            # Optional: Restrict to business days
            if demo_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                raise ValidationError("Demos are only available on weekdays.")
            
            # Optional: Restrict to next 90 days
            max_date = today + timedelta(days=90)
            if demo_date > max_date:
                raise ValidationError("Please select a date within the next 90 days.")
        
        return demo_date
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if this email has too many pending demos
        if email:
            pending_count = DemoBooking.objects.filter(
                email=email,
                status__in=['pending', 'confirmed'],
                demo_date__gte=timezone.now().date()
            ).count()
            
            if pending_count >= 3:
                raise ValidationError("You have too many pending demos. Please wait for confirmation on existing bookings.")
        
        return email.lower()
    
    def clean(self):
        cleaned_data = super().clean()
        demo_date = cleaned_data.get('demo_date')
        demo_time = cleaned_data.get('demo_time')
        
        # Check for time slot availability
        if demo_date and demo_time:
            existing_bookings = DemoBooking.objects.filter(
                demo_date=demo_date,
                demo_time=demo_time,
                status__in=['pending', 'confirmed']
            ).count()
            
            if existing_bookings >= 2:  # Limit 2 demos per time slot
                raise ValidationError(f"This time slot ({demo_time}) is already booked. Please choose another time.")
        
        return cleaned_data
    
    
class CourseEnrollmentForm(forms.ModelForm):
    """Form for course enrollment."""
    
    class Meta:
        model = CourseEnrollment
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'country', 'experience_level', 'learning_goals'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'id': 'firstName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'id': 'lastName'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'id': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'id': 'phone'
            }),
            'country': forms.Select(attrs={
                'class': 'form-control',
                'id': 'country'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'form-control',
                'id': 'experience'
            }),
            'learning_goals': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us what you hope to achieve with this course...',
                'rows': 3,
                'id': 'goals'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set country choices
        self.fields['country'].choices = [
            ('', 'Select Country'),
            ('US', 'United States'),
            ('UK', 'United Kingdom'),
            ('CA', 'Canada'),
            ('AU', 'Australia'),
            ('IN', 'India'),
            ('DE', 'Germany'),
            ('FR', 'France'),
            ('JP', 'Japan'),
            ('SG', 'Singapore'),
            ('AE', 'United Arab Emirates'),
            ('ZA', 'South Africa'),
            ('NG', 'Nigeria'),
            ('KE', 'Kenya'),
            ('GH', 'Ghana'),
        ]

class CourseFilterForm(forms.Form):
    """Form for filtering courses."""
    category = forms.ChoiceField(
        choices=[('all', 'All Courses')] + Course.CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    level = forms.ChoiceField(
        choices=[('', 'All Levels')] + Course.LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('display_order', 'Featured'),
            ('-students_enrolled', 'Most Popular'),
            ('-rating', 'Highest Rated'),
            ('price', 'Price: Low to High'),
            ('-price', 'Price: High to Low'),
            ('-created_at', 'Newest'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )