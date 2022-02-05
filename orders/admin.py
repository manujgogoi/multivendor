from django.contrib import admin
from orders.models import Order

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'product', 'price', 'quantity', 'discount', 'total', 'delivered', 'cancelled', 'paid')
    search_fields = ['customer__email', 'product__title', 'vendor__name']
    list_filter = ('created_at', 'delivered', 'delivered_at', 'paid', 'vendor')
    list_editable =['paid']
    list_per_page = 50

admin.site.register(Order, OrderAdmin)