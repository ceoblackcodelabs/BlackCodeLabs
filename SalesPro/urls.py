from django.urls import path
from .views import (
    ProductsListView,DashView,
    SoldProductsListView, AddedProductsListView,
    ExpensesListView, AddExpenses,
    OrderedProductsListView, Debts,
    AddProduct, UpdateProduct, DeleteProduct,
    DailyReportView, ContactsView, SellProduct
)

urlpatterns = [
    path('', DashView.as_view(), name='admin_dash'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('add-products-/', AddProduct.as_view(), name='add_product_'),
    path('sold-products/', SoldProductsListView.as_view(), name='sold_products'),
    path('added-products/', AddedProductsListView.as_view(), name='added_products'),
    path('products/<int:pk>/', SellProduct.as_view(), name="sellproduct"),
    path('products/update/<int:pk>/', UpdateProduct.as_view(), name='update_product'),
    path('products/delete/<int:pk>/', DeleteProduct.as_view(), name='delete_product'),
    path('ordered-products/', OrderedProductsListView.as_view(), name='ordered_products'),
    path('add-expense-/', AddExpenses.as_view(), name='add_expense'),
    path('expenses/', ExpensesListView.as_view(), name='expenses'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path("debtors/", Debts.as_view(), name='debtors'),
    path('daily-report/', DailyReportView.as_view(), name='daily_report'),
]