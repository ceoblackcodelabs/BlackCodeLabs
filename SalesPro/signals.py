from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SoldProducts, Expenses, Dashboard
from django.db.models import Sum

def update_dashboard(shop_user, expense_amount=0, is_expense_deleted=False):
    # Get or create the dashboard instance for the specific user
    dashboard, created = Dashboard.objects.get_or_create(shop=shop_user)

    # Calculate cash at hand: Total of all sold Products paid by Cash for this user
    cash_sales = SoldProducts.objects.filter(
        payment_mode='Cash',
        product__shop=shop_user
    ).aggregate(total_cash=Sum('total'))
    dashboard.cash_at_hand = cash_sales['total_cash'] or 0

    # Calculate cash at bank: Total of all sold Products paid by Till for this user
    bank_sales = SoldProducts.objects.filter(
        payment_mode='Till',
        product__shop=shop_user
    ).aggregate(total_bank=Sum('total'))
    dashboard.cash_at_bank = bank_sales['total_bank'] or 0

    # Calculate debt: Total of all sold Products with payment_mode 'Debt' for this user
    debt_sales = SoldProducts.objects.filter(
        payment_mode='Debt',
        product__shop=shop_user
    ).aggregate(total_debt=Sum('total'))
    dashboard.debt = debt_sales['total_debt'] or 0

    # Adjust cash at hand only when an expense is added
    if not is_expense_deleted:
        # If an expense was added, subtract the expense amount
        # dashboard.cash_at_hand -= expense_amount
        pass

    # Calculate total expenses: Sum of all expenses for this user
    total_expenses = Expenses.objects.filter(employee=shop_user).aggregate(total_expenses=Sum('price'))
    dashboard.expenses = total_expenses['total_expenses'] or 0

    # Calculate total sales: Cash at hand + Cash at bank + Expenses
    dashboard.total_sales = dashboard.cash_at_hand + dashboard.cash_at_bank - dashboard.expenses

    # Save the updated dashboard
    dashboard.save()

@receiver(post_save, sender=SoldProducts)
@receiver(post_delete, sender=SoldProducts)
def update_dashboard_on_sold_products(sender, instance, **kwargs):
    # Get the shop user from the product
    if instance.product and instance.product.shop:
        update_dashboard(instance.product.shop)

@receiver(post_save, sender=Expenses)
def update_dashboard_on_expenses(sender, instance, **kwargs):
    # Pass the employee (user) and price of the expense
    if instance.employee:
        update_dashboard(instance.employee, expense_amount=instance.price, is_expense_deleted=False)

@receiver(post_delete, sender=Expenses)
def update_dashboard_on_expenses_delete(sender, instance, **kwargs):
    # No need to adjust cash at hand when an expense is deleted
    if instance.employee:
        update_dashboard(instance.employee, expense_amount=instance.price, is_expense_deleted=True)