# Users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    User, SeekerProfile, SeekerSkill, Certification,
    ToolProficiency, Specialization, WorkExperience, Skill,
    DmFromResume, Company, CompanyReview, CompanySpecialization
)

User = get_user_model()

# ============= AUTHENTICATION FORMS =============

class RegisterForm(UserCreationForm):
    ACCOUNT_TYPE_CHOICES = [
        ('', 'Select account type'),
        ('Seeker', 'Seeker / Job Seeker'),
        ('Employer', 'Employer / Recruiter'),
        ('Developer', 'Developer / Admin'),
    ]

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-control',
            'id': 'register-fullname'}),
        label="Full Name",
        max_length=255,
        required=True
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'form-control',
            'id': 'register-email'}),
        label="Email Address"
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a strong password',
            'class': 'form-control',
            'id': 'register-password'}),
        label="Password"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control',
            'id': 'register-confirm-password'}),
        label="Confirm Password"
    )

    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'register-account-type'}),
        label="I am a"
    )

    agree_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'id': 'agree-terms',
            'required': 'required'}),
        label="I agree to the Terms of Service and Privacy Policy"
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2', 'account_type', 'agree_terms']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        if not cleaned_data.get("agree_terms"):
            raise ValidationError("You must agree to the terms and conditions.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.account_type = self.cleaned_data['account_type']
        user.agree_terms = self.cleaned_data['agree_terms']
        user.username = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'form-control',
            'id': 'login-email'
        }),
        label="Email Address"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
            'id': 'login-password'
        }),
        label="Password"
    )

    class Meta:
        model = User
        fields = ['username', 'password']


# ============= PROFILE FORMS =============

class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = ['pfp', 'primary_trade', 'years_experience', 'location', 'hourly_rate', 'availability']
        widgets = {
            'pfp': forms.FileInput(attrs={'class': 'file-input','accept': 'image/*'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
            'primary_trade': forms.Select(attrs={'class': 'form-select'}),
            'years_experience': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 45.00'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
        }

class SkillForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'skills-checkbox'}),
        required=False
    )

    class Meta:
        model = SeekerSkill
        fields = ['proficiency', 'years_experience']

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'expiration_date', 'credential_id', 'document']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'credential_id': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ToolProficiencyForm(forms.Form):
    TOOL_CHOICES = [
        ('power_tools', 'Power Tools'),
        ('hand_tools', 'Hand Tools'),
        ('heavy_equipment', 'Heavy Equipment'),
        ('diagnostic_equipment', 'Diagnostic Equipment'),
        ('welding_equipment', 'Welding Equipment'),
        ('plumbing_tools', 'Plumbing Tools'),
    ]

    tools = forms.MultipleChoiceField(
        choices=TOOL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tool-checkbox'}),
        required=False
    )

class SpecializationForm(forms.Form):
    SPECIALIZATION_CHOICES = [
        ('commercial_projects', 'Commercial Projects'),
        ('residential_work', 'Residential Work'),
        ('industrial_maintenance', 'Industrial Maintenance'),
        ('new_construction', 'New Construction'),
        ('renovation', 'Renovation'),
        ('emergency_services', 'Emergency Services'),
    ]

    specializations = forms.MultipleChoiceField(
        choices=SPECIALIZATION_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'specialization-chip'}),
        required=False
    )

class ContactTalentForm(forms.ModelForm):
    class Meta:
        model = DmFromResume
        fields = ['name', 'email', 'subject', 'project_type', 'description', 'location', 'contact', 'link']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email', 'required': 'required'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Subject', 'required': 'required'}),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Description', 'rows': 4, 'required': 'required'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State', 'required': 'required'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'required': 'required'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Project Link (optional)'}),
        }

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        # Allow longer phone numbers
        if contact and len(contact) > 20:
            raise forms.ValidationError("Phone number is too long. Max 20 characters.")
        return contact

# ============= COMPANY PROFILE FORMS =============

class CompanyProfileForm(forms.ModelForm):
    """
    Form for updating company profile information
    """
    class Meta:
        model = Company
        fields = [
            'name', 'industry', 'location', 'description',
            'website', 'email', 'phone', 'year_founded', 'pfp'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name',
                'required': 'required'
            }),
            'industry': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Software Development, Construction, Healthcare'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your company...',
                'rows': 5
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourcompany.com'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@company.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'year_founded': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2020',
                'min': 1800,
                'max': 2025
            }),
            'pfp': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': 'image/*'
            }),
        }
        labels = {
            'name': 'Company Name',
            'industry': 'Industry',
            'location': 'Headquarters Location',
            'description': 'Company Description',
            'website': 'Company Website',
            'email': 'Company Email',
            'phone': 'Contact Phone',
            'year_founded': 'Year Founded',
            'pfp': 'Company Logo',
        }

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            website = f'https://{website}'
        return website

    def clean_year_founded(self):
        year = self.cleaned_data.get('year_founded')
        current_year = timezone.now().year
        if year and year > current_year:
            raise forms.ValidationError("Year founded cannot be in the future.")
        if year and year < 1800:
            raise forms.ValidationError("Please enter a valid year.")
        return year


class CompanySpecializationForm(forms.Form):
    """
    Form for managing company specializations
    """
    COMPANY_SPECIALIZATION_CHOICES = [
        ('web_development', 'Web Development'),
        ('mobile_development', 'Mobile App Development'),
        ('ai_ml', 'AI & Machine Learning'),
        ('cloud_services', 'Cloud Services'),
        ('cybersecurity', 'Cybersecurity'),
        ('devops', 'DevOps & Infrastructure'),
        ('ui_ux_design', 'UI/UX Design'),
        ('data_analytics', 'Data Analytics'),
        ('erp_solutions', 'ERP Solutions'),
        ('crm_development', 'CRM Development'),
        ('ecommerce', 'E-Commerce Solutions'),
        ('digital_marketing', 'Digital Marketing'),
        ('it_consulting', 'IT Consulting'),
        ('software_testing', 'Software Testing & QA'),
        ('maintenance_support', 'Maintenance & Support'),
    ]

    specializations = forms.MultipleChoiceField(
        choices=COMPANY_SPECIALIZATION_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'specialization-checkbox'}),
        required=False,
        label="Company Specializations"
    )


class CompanyReviewForm(forms.ModelForm):
    """
    Form for submitting company reviews
    """
    class Meta:
        model = CompanyReview
        fields = ['name', 'email', 'service', 'review_text', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': 'required'
            }),
            'service': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What service did you receive?',
                'rows': 2,
                'required': 'required'
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience with this company...',
                'rows': 5,
                'required': 'required'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rating (1-5)',
                'min': 1,
                'max': 5,
                'required': 'required'
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not '@' in email:
            raise forms.ValidationError("Enter a valid email address.")
        return email