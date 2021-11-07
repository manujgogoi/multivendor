from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from stores.models import Category, Product, Image, Specification

class ImageInline(admin.TabularInline):
    model = Image

class SpecificationInline(admin.TabularInline):
    model = Specification
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
        SpecificationInline
    ]

# Register your models here.
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
admin.site.register(Specification)