# Home/forms.py
from django import forms
from django.core.validators import RegexValidator
from .models import ContactInquiry

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