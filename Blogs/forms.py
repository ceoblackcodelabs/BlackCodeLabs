from django import forms
from .models import Comment, ContactMessage


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={
                "class": "textarea",
                "rows": 4,
                "placeholder": "Share your thoughts respectfully...",
            }),
        }
        labels = {"body": "Your comment"}


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Jane Doe"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "jane@school.edu"}),
            "subject": forms.TextInput(attrs={"class": "input", "placeholder": "How can we help?"}),
            "message": forms.Textarea(attrs={"class": "textarea", "rows": 6, "placeholder": "Write your message..."}),
        }


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


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
