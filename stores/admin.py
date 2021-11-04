from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from stores.models import Category, Product, Image, Specification

# Register your models here.
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Specification)