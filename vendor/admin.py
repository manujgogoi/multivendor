from django.contrib import admin
from .models import Vendor

# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')

admin.site.register(Vendor, VendorAdmin)