# Home/forms.py
from django import forms
from django.core.validators import RegexValidator, validate_email
import re
from decimal import Decimal
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
    
    course_id = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = CourseEnrollment
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'country', 'experience_level', 'learning_goals',
            'course_id'
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
                'placeholder': 'Enter your email address',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter your phone number',
                'class': 'form-control'
            }),
            'country': forms.Select(attrs={
                'class': 'form-control'
            }),
            'experience_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'learning_goals': forms.Textarea(attrs={
                'placeholder': 'Tell us what you hope to achieve with this course...',
                'class': 'form-control',
                'rows': 4
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize country choices if needed
        self.fields['country'].widget.choices = [
            ('', 'Select Country'),
            ('US', 'United States'),
            ('CA', 'Canada'),
            ('GB', 'United Kingdom'),
            ('AU', 'Australia'),
            ('IN', 'India'),
            ('DE', 'Germany'),
            ('FR', 'France'),
            ('JP', 'Japan'),
            ('SG', 'Singapore'),
            ('AE', 'United Arab Emirates'),
            # African Countries
            ('ZA', 'South Africa'),
            ('NG', 'Nigeria'),
            ('KE', 'Kenya'),
            ('GH', 'Ghana'),
            ('ET', 'Ethiopia'),
            ('EG', 'Egypt'),
            ('TZ', 'Tanzania'),
            ('UG', 'Uganda'),
            ('DZ', 'Algeria'),
            ('SD', 'Sudan'),
            ('MA', 'Morocco'),
            ('AO', 'Angola'),
            ('MZ', 'Mozambique'),
            ('CI', 'Côte d\'Ivoire'),
            ('MG', 'Madagascar'),
            ('CM', 'Cameroon'),
        ]
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if not first_name:
            raise ValidationError('First name is required.')
        if len(first_name) < 2:
            raise ValidationError('First name must be at least 2 characters.')
        if not re.match(r'^[A-Za-z\s\-]+$', first_name):
            raise ValidationError('First name can only contain letters, spaces, and hyphens.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if not last_name:
            raise ValidationError('Last name is required.')
        if len(last_name) < 2:
            raise ValidationError('Last name must be at least 2 characters.')
        if not re.match(r'^[A-Za-z\s\-]+$', last_name):
            raise ValidationError('Last name can only contain letters, spaces, and hyphens.')
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError('Email is required.')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Please enter a valid email address.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError('Phone number is required.')
        
        # Allow various phone formats
        phone_regex = r'^[\+]?[1-9][\d]{0,15}$'
        if not re.match(phone_regex, phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            raise ValidationError('Please enter a valid phone number.')
        return phone
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise ValidationError('Please select your country.')
        return country
    
    def clean_experience_level(self):
        experience_level = self.cleaned_data.get('experience_level')
        if not experience_level:
            raise ValidationError('Please select your experience level.')
        return experience_level
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Additional cross-field validation
        email = cleaned_data.get('email')
        course_id = cleaned_data.get('course_id')
        
        # Check if email is already enrolled in this course
        if email and course_id:
            from .models import Course, CourseEnrollment
            try:
                course = Course.objects.get(id=course_id)
                if CourseEnrollment.objects.filter(email=email, course=course).exists():
                    self.add_error('email', 'This email is already enrolled in this course.')
            except Course.DoesNotExist:
                self.add_error('course_id', 'Invalid course selected.')
        
        return cleaned_data

# Additional Forms for Admin

class CourseForm(forms.ModelForm):
    """Form for creating/editing courses."""
    
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'detailed_description': forms.Textarea(attrs={'rows': 10}),
            'instructor_bio': forms.Textarea(attrs={'rows': 5}),
            'details': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': '{"Mode": "Online", "Schedule": "Mon & Wed"}'
            }),
            'curriculum': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': '[{"title": "Module 1", "lessons": ["Lesson 1", "Lesson 2"]}]'
            }),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
    
    def clean_details(self):
        details = self.cleaned_data.get('details')
        if details:
            try:
                import json
                json.loads(details)
            except json.JSONDecodeError:
                raise ValidationError('Details must be valid JSON format.')
        return details
    
    def clean_curriculum(self):
        curriculum = self.cleaned_data.get('curriculum')
        if curriculum:
            try:
                import json
                data = json.loads(curriculum)
                if not isinstance(data, list):
                    raise ValidationError('Curriculum must be a JSON array.')
            except json.JSONDecodeError:
                raise ValidationError('Curriculum must be valid JSON format.')
        return curriculum

class EnrollmentStatusForm(forms.ModelForm):
    """Form for updating enrollment status."""
    
    class Meta:
        model = CourseEnrollment
        fields = ['status', 'payment_status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }