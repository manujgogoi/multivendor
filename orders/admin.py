from django.contrib import admin
from orders.models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'product', 'price', 'quantity', 'discount', 'total', 'completed', 'cancelled', 'paid')

admin.site.register(Order, OrderAdmin)