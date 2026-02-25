from django.shortcuts import render
from django.views.generic import (
    ListView, CreateView, View as DjangoView,
    UpdateView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    OrderedProducts, Dashboard as Dashmodel,
    Products, SoldProducts, MessageUser,
    AddedProducts, Expenses, Contact,
    Employee
    )
from django.urls import reverse_lazy
from .forms import (
    ProductsForm, ExpenseForm, ContactForm,
    SoldProductsForm
)
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponse
import pytz
from datetime import datetime
import random, string

# pdfgen
from django.http import HttpResponse
import weasyprint
from django.template.loader import render_to_string
import base64
from django.conf import settings

from django.template.loader import get_template
from datetime import datetime

# automatic reset
from django.db import transaction

# timezone kenya
kenya_timezone = pytz.timezone('Africa/Nairobi')
utc_now = datetime.now(pytz.utc)# Getting the current time in UTC
kenya_time = utc_now.astimezone(kenya_timezone)

# Create your views here.
class DashView(LoginRequiredMixin, ListView):
    model = OrderedProducts
    context_object_name = 'products'
    template_name = 'Store/dash.html'
    paginate_by = 25

    def get_queryset(self):
        # Filter ordered products by the current user's shop
        return OrderedProducts.objects.filter(
            product__shop=self.request.user
        ).select_related('product').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(shop=self.request.user)
        dashdata = [
            float(dashboard.total_sales or 0),
            float(dashboard.cash_at_hand or 0),
            float(dashboard.cash_at_bank or 0),
            float(dashboard.expenses or 0),
            float(dashboard.debt or 0)
        ]

        low_stock_products = Products.objects.filter(
            shop=self.request.user,
            closing_stock__lte=20
        )[:10]

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        context['dashdata'] = dashdata
        context['productsB20'] = [p.name for p in low_stock_products]  # Product names
        context['productsidB20'] = [p.closing_stock for p in low_stock_products]  # Stock values
        return context


class ProductsListView(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'Store/products.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        dashdata = [dashboard.total_sales, dashboard.cash_at_hand, dashboard.cash_at_bank, dashboard.expenses, dashboard.debt]

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        context['dashdata'] = dashdata
        context['productsB20'] = [product.abv for index, product in enumerate(Products.objects.all()) if product.closing_stock <= 20]
        context['productsidB20'] = [product.closing_stock for index, product in enumerate(Products.objects.all()) if product.closing_stock <= 20]
        return context


class SoldProductsListView(LoginRequiredMixin, ListView):
    model = SoldProducts
    template_name = 'Store/sold_products.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        dashdata = [dashboard.total_sales, dashboard.cash_at_hand, dashboard.cash_at_bank, dashboard.expenses, dashboard.debt]

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        context['dashdata'] = dashdata
        context['productsB20'] = [product.product.abv for index, product in enumerate(SoldProducts.objects.all())]
        context['productsidB20'] = [product.product.closing_stock for index, product in enumerate(SoldProducts.objects.all())]
        context['kenya_time'] = kenya_time
        return context

class AddedProductsListView(LoginRequiredMixin, ListView):
    model = AddedProducts
    template_name = 'Store/added_products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        context['dashboard'] = dashboard
        context['kenya_time'] = kenya_time
        return context

class AddProduct(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'Store/add_product.html'
    success_url = reverse_lazy('products_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context


class DeleteProduct(LoginRequiredMixin, DjangoView):
    def get(self, request, pk):
        product = get_object_or_404(Products, pk=pk)
        product.delete()
        return redirect('products_list')

class UpdateProduct(LoginRequiredMixin, UpdateView):
    model = Products
    form_class = ProductsForm
    template_name = 'Store/update_product.html'
    success_url = reverse_lazy('products_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class OrderedProductsListView(LoginRequiredMixin, ListView):
    model = OrderedProducts
    context_object_name = 'products'
    template_name = 'Store/orderd.html'

    def get_queryset(self):
        # Filter ordered products by current user's shop
        return OrderedProducts.objects.filter(product__shop=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve or create the Dashboard instance for the current user
        dashboard, created = Dashmodel.objects.get_or_create(shop=self.request.user)

        # Filter products by current user's shop
        user_products = Products.objects.filter(shop=self.request.user)

        top_5_products_label = [product.name for product in user_products.order_by('-sold_stock')[:5]]
        top_5_product_data = [product.sold_stock for product in user_products.order_by('-sold_stock')[:5]]
        context['top_5_products_data'] = top_5_product_data
        context['top_5_products_label'] = top_5_products_label

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class ExpensesListView(LoginRequiredMixin, ListView):
    model = Expenses
    template_name = 'Store/expenses.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class AddExpenses(LoginRequiredMixin, DjangoView):
    def get(self, request):
        form = ExpenseForm()
        # Get or create the Dashboard instance
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        # Pass dashboard to the context
        return render(request, 'Store/add_expense.html', {'form': form, 'dashboard': dashboard})

    def post(self, request):
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.employee = request.user
            expense.save()
            messages.success(request, 'Expense added successfully')
            return redirect('expenses')

        # Get or create the Dashboard instance
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)
        # Pass dashboard to the context
        return render(request, 'Store/add_expense.html', {'form': form, 'dashboard': dashboard})

class Debts(LoginRequiredMixin, ListView):
    model = SoldProducts
    context_object_name = 'debtors'
    template_name = 'Store/debts.html'

    def get_queryset(self):
        # Filter to only include debts
        return super().get_queryset().filter(status='Debt')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the Dashboard instance, or create one if it doesn't exist
        dashboard, created = Dashmodel.objects.get_or_create(pk=1)

        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        return context

class ContactsView(LoginRequiredMixin, ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'Home/contacts.html'

    def get_queryset(self):
        # Filter contacts by current user's shop (if Contact model has shop field)
        # If Contact model doesn't have shop field, you might need to add it
        return Contact.objects.filter(shop=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve or create the Dashboard instance for the current user
        dashboard, created = Dashmodel.objects.get_or_create(shop=self.request.user)
        # Add the Dashboard instance to the context
        context['dashboard'] = dashboard
        # Add the ContactForm to the context
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            # If Contact model has shop field, assign current user
            if hasattr(contact, 'shop'):
                contact.shop = request.user
            contact.save()
            return redirect('contacts')

        # If the form is not valid, render the template with the full context
        context = self.get_context_data()
        context['form'] = form  # Pass the invalid form to the context
        return self.render_to_response(context)

class SellProduct(DetailView):
    model = Products
    context_object_name = "product"
    template_name = 'Store/selling_form.html'

    def get_queryset(self):
        return Products.objects.filter(shop=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve or create the Dashboard instance for the current user
        dashboard, created = Dashmodel.objects.get_or_create(shop=self.request.user)

        # Filter products by current user's shop
        user_products = Products.objects.filter(shop=self.request.user)

        top_5_products_label = [product.name for product in user_products.order_by('-sold_stock')[:5]]
        top_5_product_data = [product.sold_stock for product in user_products.order_by('-sold_stock')[:5]]
        context['top_5_products_data'] = top_5_product_data
        context['top_5_products_label'] = top_5_products_label
        context['dashboard'] = dashboard
        context['form'] = SoldProductsForm()
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()  # Get the current product object
        form = SoldProductsForm(request.POST)
        if form.is_valid():
            sold_product = form.save(commit=False)
            sold_product.product = product
            sold_product.save()
            product.save()  # Save the product if necessary
            return redirect('sold_products')

        # If the form is not valid, get the full context and pass the form
        context = self.get_context_data()
        context['form'] = form  # Update the context with the invalid form
        return self.render_to_response(context)

class EmployeesView(LoginRequiredMixin, ListView):
    model = Employee

class DailyReportView(View):
    def get(self, request, *args, **kwargs):
        today = kenya_time

        # Fetch data for the report - filtered by current user
        dashboard, created = Dashmodel.objects.get_or_create(shop=request.user)
        sold_products = SoldProducts.objects.filter(date__date=today, product__shop=request.user)
        expenses = Expenses.objects.filter(date__date=today, employee=request.user)
        products = Products.objects.filter(shop=request.user)
        debts = SoldProducts.objects.filter(status='Debt', product__shop=request.user)

        # Calculate totals
        total_sales = sum(product.total for product in sold_products)
        total_expenses = sum(expense.price for expense in expenses)
        stocks_added = sum(product.added_stock for product in products)
        stocks_sold = sum(product.sold_stock for product in products)

        # Encode logo as Base64
        logo_path = settings.BASE_DIR / 'Home/static/assets/images/logo.png'
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Prepare the data for the preview
        context = {
            'dashboard': dashboard,
            'products': products,
            'total_sales': total_sales,
            'total_expenses': total_expenses,
            'stocks_added': stocks_added,
            'stocks_sold': stocks_sold,
            'sold_products': sold_products,
            'expenses': expenses,
            'today': today,
            'debts': debts,
            'logo_base64': logo_base64,
        }
        return render(request, 'Email/report.html', context)

    def post(self, request, *args, **kwargs):
        today = kenya_time

        # Fetch data for the report - filtered by current user
        dashboard, created = Dashmodel.objects.get_or_create(shop=request.user)
        sold_products = SoldProducts.objects.filter(date__date=today, product__shop=request.user)
        expenses = Expenses.objects.filter(date__date=today, employee=request.user)
        products = Products.objects.filter(shop=request.user)
        debts = SoldProducts.objects.filter(status='Debt', product__shop=request.user)

        # Calculate totals
        total_sales = sum(product.total for product in sold_products)
        total_expenses = sum(expense.price for expense in expenses)
        stocks_added = sum(product.added_stock for product in products)
        stocks_sold = sum(product.sold_stock for product in products)

        # Encode logo as Base64
        logo_path = settings.BASE_DIR / 'Home/static/assets/images/logo.png'
        with open(logo_path, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # Prepare the context for the PDF
        context = {
            'dashboard': dashboard,
            'debts': debts,
            'products': products,
            'total_sales': total_sales,
            'total_expenses': total_expenses,
            'stocks_added': stocks_added,
            'stocks_sold': stocks_sold,
            'sold_products': sold_products,
            'expenses': expenses,
            'today': today,
            'report_id': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)),
            'logo_base64': logo_base64,
        }

        # Render the HTML template to a string
        html_content = render_to_string('Email/post_report.html', context)

        # Create the PDF from HTML using WeasyPrint
        pdf_file = weasyprint.HTML(string=html_content).write_pdf()

        # Create an HTTP response with the PDF content
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{today}-report.pdf"'

        # Update and reset models after report generation - only for current user
        with transaction.atomic():  # Ensure all updates happen in a single transaction
            # Update `Products` model for current user
            for product in Products.objects.filter(shop=request.user):
                product.opening_stock = product.closing_stock  # Set opening stock to closing stock
                product.added_stock = 0  # Reset added stock
                product.sold_stock = 0  # Reset sold stock
                product.save()

            # Delete today's SoldProducts records for current user
            SoldProducts.objects.filter(date__date=today, product__shop=request.user).delete()

            # Reset Expenses for today for current user
            Expenses.objects.filter(date__date=today, employee=request.user).delete()

            # Reset debtors for current user
            SoldProducts.objects.filter(status='Debt', product__shop=request.user).delete()

            # Reset Order for current user
            OrderedProducts.objects.filter(start_date__date=today, product__shop=request.user).delete()

        return response