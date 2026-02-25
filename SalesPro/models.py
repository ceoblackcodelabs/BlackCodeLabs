from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
import random, string
from colorama import Fore, Style, Back
import pytz
from .email import send_email
from django.contrib import messages
from django.utils import timezone

# timezone kenya
kenya_timezone = pytz.timezone('Africa/Nairobi')
utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
kenya_time = utc_now.astimezone(kenya_timezone)

class Dashboard(models.Model):
    shop = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cash_at_hand = models.IntegerField(default=0, null=True)
    cash_at_bank = models.IntegerField(default=0, null=True)
    expenses = models.IntegerField(default=0, null=True)
    total_sales = models.IntegerField(default=0, null=True)
    debt = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f"Dashboard - {self.shop.username if self.shop else 'No Shop'}"

    class Meta:
        unique_together = ['shop']  # Ensure each user has only one dashboard


class Products(models.Model):
    shop = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField("Product Name", max_length=50, default="")
    abv = models.CharField(max_length=3, default='', null=True, blank=True)
    wholesale = models.IntegerField(null=True)
    cost = models.IntegerField(default=100)
    opening_stock = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    added_stock = models.IntegerField(default=0)
    sold_stock = models.IntegerField(default=0)
    closing_stock = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Only calculate closing stock if this is a new save (not from SoldProducts)
        # Calculate the closing stock
        self.closing_stock = self.opening_stock + self.added_stock - self.sold_stock

        super(Products, self).save(*args, **kwargs)  # Save the instance first

        # Only check for low stock if this is a regular save (not from update_fields)
        if 'update_fields' not in kwargs and self.closing_stock < 6:
            print(f"{Back.RED} {self.name} is running low. Stock left: {self.closing_stock} {Style.RESET_ALL}")

            from .models import OrderedProducts

            # Check if an order already exists for this product and is still pending
            existing_order = OrderedProducts.objects.filter(product=self, order_status='pending').first()
            if not existing_order:
                # Create an order if no pending order exists
                OrderedProducts.objects.create(
                    product=self,
                    product_cost=self.cost,
                    payment_mode='Cash',
                    order_status='pending'
                )
                print(f"{Back.GREEN} Order made successfully {Back.RESET}")

                # Retrieve all superuser accounts
                superusers = User.objects.filter(is_superuser=True)
                superuser_emails = [user.email for user in superusers]
                if superuser_emails:
                    for su_email in superuser_emails:
                        # send_email(
                        #     product=self.name,
                        #     date=kenya_time,
                        #     email=f'{su_email}'
                        # )
                        print(f"{Back.GREEN} Email sent successfully to {su_email} {Back.RESET}")
                else:
                    print(f'{Back.RED} No email found {Style.RESET_ALL}')

    def __str__(self):
        return f"{self.name} - {self.shop.username if self.shop else 'No Shop'}"

    class Meta:
        ordering = ['-date_added']
        unique_together = ['shop', 'name']


class SoldProducts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='sold_products')
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default='paid', null=False, choices=(
        ('Paid', 'Paid'),
        ('Debt', 'Debt')
    ))
    total = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=50, null=True, choices=(
        ('Till', 'Till'),
        ('Cash', 'Cash'),
        ('Debt', 'Debt'),
    ))
    customer = models.CharField(max_length=50, null=False, default='')
    customer_contact = models.CharField(max_length=20, default='+254')
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        # Set sold_by if not set (you'll need to pass request user from view)

        # Calculate the total price
        self.total = self.quantity * self.product.cost

        # Check if there is enough stock available
        available_stock = self.product.opening_stock + self.product.added_stock - self.product.sold_stock
        if self.quantity > available_stock:
            raise ValidationError(f"Cannot sell {self.quantity} of {self.product.name}. Available stock is only {available_stock}.")

        # Update the product's sold stock
        self.product.sold_stock += self.quantity

        # Update closing stock directly without calling product.save() to avoid circular save
        self.product.closing_stock = self.product.opening_stock + self.product.added_stock - self.product.sold_stock

        # Save the product WITHOUT triggering the Products.save() method again
        super(Products, self.product.__class__).save(self.product, update_fields=['sold_stock', 'closing_stock'])

        super(SoldProducts, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"


class AddedProducts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Add this field
    date_added = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add to default

    def __str__(self):
        return f"Added {self.product.name}"


class Expenses(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.CharField(max_length=100, default='', null=False, blank=False)
    price = models.IntegerField(default=100, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True, null=True)
    shop = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_expenses', blank=True, null=True)  # Add this field

    def save(self, *args, **kwargs):
        # timezone kenya
        kenya_timezone = pytz.timezone('Africa/Nairobi')
        utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
        kenya_time = utc_now.astimezone(kenya_timezone)
        self.date = kenya_time

        # Set the shop to the employee's shop if not set
        if not self.shop:
            self.shop = self.employee

        super(Expenses, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.expense} - {self.employee.username}"


class OrderedProducts(models.Model):
    ORDER_STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    PAYMENT_MODE = [
        ('M-pesa', 'M-pesa'),
        ('Cash', 'Cash'),
    ]

    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='ordered_products')
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE)
    start_date = models.DateTimeField('DateTime Ordered', auto_now_add=True)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Add this field

    def save(self, *args, **kwargs):
        # Generate a unique order number if it hasn't been set yet
        if not self.order_number:
            self.order_number = self.generate_order_number()

        # timezone kenya
        kenya_timezone = pytz.timezone('Africa/Nairobi')
        utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
        kenya_time = utc_now.astimezone(kenya_timezone)
        self.start_date = kenya_time

        # Set ordered_by to the product's shop if not set
        if not self.ordered_by and self.product.shop:
            self.ordered_by = self.product.shop

        super().save(*args, **kwargs)

    def generate_order_number(self):
        # Generate a random string of 6 characters (letters and digits)
        random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"ORD-{random_chars}"

    def __str__(self):
        return f"Order {self.order_number} - {self.product.name}"

    def clean(self):
        # Custom validation logic can be added here
        if self.product_cost < 0:
            raise ValidationError("Product cost cannot be negative.")


class Contact(models.Model):
    shop = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Add this field
    name = models.CharField(max_length=50, default="")
    contact = models.CharField(max_length=20, default='+254')
    role = models.CharField(max_length=50, default='Supplier')
    location = models.CharField(max_length=50, default='Nairobi')
    picture = models.ImageField(upload_to='Contact', null=True, default='Contact/default.png')

    def __str__(self):
        return f"{self.name} -> {self.role} - {self.shop.username if self.shop else 'No Shop'}"

    class Meta:
        unique_together = ['shop', 'name', 'contact']  # Ensure contacts are unique per shop


class MessageUser(models.Model):
    shop = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Add this field
    name = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    date_sent = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add to default

    def __str__(self):
        return f"Message to {self.name.name} - {self.shop.username if self.shop else 'No Shop'}"


class Employee(models.Model):
    shop = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Add this field
    name = models.CharField(max_length=50, default="")
    salary = models.IntegerField(default=0)
    contact = models.CharField(max_length=20, default='+254')
    role = models.CharField(max_length=50, default='Employee')
    location = models.CharField(max_length=50, default='Nairobi')
    picture = models.ImageField(upload_to='Employee', null=True, default='Employee/default.png')

    def __str__(self):
        return f"{self.name} -> {self.role} - {self.shop.username if self.shop else 'No Shop'}"

    class Meta:
        unique_together = ['shop', 'name', 'contact']  # Ensure employees are unique per shop