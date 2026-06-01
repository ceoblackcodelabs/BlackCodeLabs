from django import forms
from django.core.validators import RegexValidator
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Form for contact page submissions"""

    # Custom subject field for 'other' option
    subject_other = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Please specify your subject'
        })
    )

    # Phone number validation (Kenyan format example)
    phone = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9]{10,15}$',
                message='Enter a valid phone number (e.g., +254799804185)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+254 799 804 185'
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        subject_other = cleaned_data.get('subject_other')

        # Validate subject_other when 'other' is selected
        if subject == 'other' and not subject_other:
            self.add_error('subject_other', 'Please specify your subject')

        return cleaned_data

    def save(self, commit=True, request=None):
        instance = super().save(commit=False)

        # Set subject_other if provided
        if instance.subject == 'other':
            instance.subject_other = self.cleaned_data.get('subject_other')

        # Capture request metadata
        if request:
            instance.ip_address = self._get_client_ip(request)
            instance.user_agent = request.META.get('HTTP_USER_AGENT', '')

        if commit:
            instance.save()

        return instance

    def _get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip