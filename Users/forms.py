from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "input", "placeholder": "you@school.edu"}))
    first_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={"class": "input", "placeholder": "Jane"}))
    last_name = forms.CharField(max_length=60, required=False, widget=forms.TextInput(attrs={"class": "input", "placeholder": "Doe"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input", "placeholder": "janedoe"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("password1", "password2"):
            self.fields[name].widget.attrs.update({"class": "input", "placeholder": "••••••••"})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "input", "placeholder": "Username", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "••••••••"}))
