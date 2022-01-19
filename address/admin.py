from django.contrib import admin
from address.models import State, District, PIN, VillageOrTown
# Register your models here.

class VillageOrTownInline(admin.TabularInline):
    model = VillageOrTown

class PINInline(admin.TabularInline):
    model = PIN

class DistrictInline(admin.TabularInline):
    model = District

class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_deliverable')
    list_editable = ['is_deliverable']
    list_filter = ['is_deliverable']
    inlines = [
        DistrictInline
    ]

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_deliverable')
    list_editable = ['is_deliverable']
    list_filter = ['is_deliverable']
    inlines = [
        PINInline
    ]

class PINAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_deliverable')
    list_editable = ['is_deliverable']
    list_filter = ['is_deliverable']
    inlines = [
        VillageOrTownInline
    ]

class VillageOrTownAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_deliverable')
    list_editable = ['is_deliverable']
    list_filter = ['is_deliverable']


#Register models
admin.site.register(VillageOrTown, VillageOrTownAdmin)
admin.site.register(PIN, PINAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(State, StateAdmin)