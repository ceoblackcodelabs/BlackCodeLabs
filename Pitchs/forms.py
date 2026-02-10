from django import forms
from django.core.validators import RegexValidator
from .models import ProjectRequest, Project

class ProjectRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectRequest
        fields = ['project', 'custom_title', 'description', 'phone_number', 'email']
        widgets = {
            'project': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select an existing project or leave blank for custom'
            }),
            'custom_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your project title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your project requirements in detail',
                'rows': 4
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +254712345678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available projects in the dropdown
        self.fields['project'].queryset = Project.objects.filter(is_available=True)
        self.fields['project'].required = False
        self.fields['project'].label = "Select Existing Project (Optional)"