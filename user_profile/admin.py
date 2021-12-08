from django.contrib import admin
from user_profile.models import Profile, DeliveryAddress
# Register your models here.

class DeliveryAddressInline(admin.TabularInline):
    model = DeliveryAddress

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'is_phone_verified')
    list_editable = ['is_phone_verified']
    list_filter = ['is_phone_verified']
    inlines = [DeliveryAddressInline]


# Register models to admin
admin.site.register(Profile, ProfileAdmin)