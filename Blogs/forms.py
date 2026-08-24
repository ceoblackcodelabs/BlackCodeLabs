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
                "placeholder": "Share your thoughts...",
            }),
        }
        labels = {"body": "Your comment"}


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Jane Doe"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "jane@example.com"}),
            "subject": forms.TextInput(attrs={"class": "input", "placeholder": "How can we help?"}),
            "message": forms.Textarea(attrs={"class": "textarea", "rows": 6, "placeholder": "Write your message..."}),
        }
