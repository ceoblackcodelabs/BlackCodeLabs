from django.contrib import admin
from . import models as StoreModel

admin.site.site_header = 'SalesPro Dev'
admin.site.index_title = 'DevAdmin'

@admin.register(StoreModel.Dashboard)
class AdminDash(admin.ModelAdmin):
    list_display = [field.name for field in StoreModel.Dashboard._meta.get_fields()]

@admin.register(StoreModel.Products)
class AdminProducts(admin.ModelAdmin):
    list_display = ('name', 'abv', 'wholesale', 'cost', 'opening_stock', 'added_stock', 'sold_stock', 'closing_stock')

@admin.register(StoreModel.AddedProducts)
class AdminAddedProducts(admin.ModelAdmin):
    list_display = ['product']

@admin.register(StoreModel.SoldProducts)
class  AdminSoldProducts(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'status', 'total' ,'date')

@admin.register(StoreModel.OrderedProducts)
class OrderedProductsAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'product', 'product_cost', 'payment_mode', 'start_date', 'order_status')
    search_fields = ('order_number', 'product__name', 'payment_mode')
    list_filter = ('order_status', 'payment_mode')
    ordering = ('-start_date',)

@admin.register(StoreModel.Contact)
class RegContact(admin.ModelAdmin):
    list_display = ['name', 'contact', 'role', 'location']

@admin.register(StoreModel.MessageUser)
class RegMessage(admin.ModelAdmin):
    list_display = ['name', 'message']

@admin.register(StoreModel.Employee)
class AdminEmployee(admin.ModelAdmin):
    list_display = [field.name for field in StoreModel.Employee._meta.get_fields()]

@admin.register(StoreModel.Expenses)
class AdminExpens(admin.ModelAdmin):
    list_display = [field.name for field in StoreModel.Expenses._meta.get_fields()]