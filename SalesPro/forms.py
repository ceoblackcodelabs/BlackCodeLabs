from django import forms
from .models import (
    Products, Expenses, Contact,
    MessageUser, SoldProducts
)


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'wholesale', 'cost', 'opening_stock', 'added_stock', 'sold_stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Product Name'}),
            'wholesale': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Wholesale Price'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Cost'}),
            'opening_stock': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Opening Stock'}),
            'added_stock': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Added Stock'}),
            'sold_stock': forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Sold Stocks'}),
        }

class ContactForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Message'}))
    name = forms.ModelChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control p_input'}),
        empty_label="Select User"
    )

    class Meta:
        model = MessageUser
        fields = ['message', 'name']


class ExpenseForm(forms.ModelForm):
    expense = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter The Expense'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter price'}))
    class Meta:
        model = Expenses
        fields = ['expense', 'price']


class SoldProductsForm(forms.ModelForm):
    quantity = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Quantity'}))
    status = forms.ChoiceField(
        choices=(
            ('Paid', 'Paid'),
            ('Debt', 'Debt')
        ),
        widget=forms.Select(attrs={'class': 'form-control p_input'})
    )
    payment_mode = forms.ChoiceField(
        choices=(
            ('Till', 'Till'),
            ('Cash', 'Cash'),
            ('Debt', 'Debt')
        ),
        widget=forms.Select(attrs={'class': 'form-control p_input'})
    )
    customer = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Customer Name'}))
    customer_contact = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Customer Number 0712345678'}))

    class Meta:
        model = SoldProducts
        fields = ['quantity', 'status', 'customer', 'customer_contact', 'payment_mode']























from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

class UserReg(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Confirm Password'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input", 'type': "checkbox"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_superuser']:
            user.is_superuser = True
            user.is_staff = True  # Superusers are also staff members
        if commit:
            user.save()
        return user

class UserChange(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Enter Password'}), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control p_input', 'placeholder': 'Confirm Password'}), required=False)
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input", 'type': "checkbox"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['is_superuser']:
            user.is_superuser = True
            user.is_staff = True  # Superusers are also staff members
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove labels and add placeholders for username and password fields
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs.update({
            'class': 'form-control p_input',
            'placeholder': 'Enter Username'
        })

        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({
            'class': 'form-control p_input',
            'placeholder': 'Enter Password'
        })

class ContactForm(forms.Form):
    Name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    Title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}))
    Description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Comment', 'rows': 4}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        # Remove labels for all fields
        self.fields['Name'].label = ''
        self.fields['Email'].label = ''
        self.fields['Title'].label = ''
        self.fields['Description'].label = ''
