# Users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import (
    User, SeekerProfile, SeekerSkill, Certification,
    ToolProficiency, Specialization, WorkExperience, Skill,
    DmFromResume
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