from django.contrib import admin
from carriers.models import Carrier
from orders.models import Order

# Register your models here. 

class CarrierAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {'fields' : ('user', ('first_name', 'middle_name'), 'last_name')}),
        ('Address', {
            'classes': ('collapse',),
            'fields' : (
                ('house_no', 'landmark'), ('vill_or_town', 'district'), ('state', 'country'), 'pin_code'
                )
            }
        ),
        ('Contact', {'fields': (('mobile_no', 'mobile_verified'),)}),
        ('Id Proof', {'fields': ('id_proof_type', 'id_proof_number', 'id_proof_document')}),
        ('Address Proof', {'fields': ('address_proof_type', 'address_proof_number', 'address_proof_document')}),
        ('Controls', {'fields': ('is_active',)})
        
    )

    list_display=['id', 'first_name', 'last_name', 'mobile_no', 'vill_or_town', 'is_active']
    list_display_links = ('first_name', 'last_name')

admin.site.register(Carrier, CarrierAdmin)
