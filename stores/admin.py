from django.contrib import admin
from stores.models import Category, Product, Image, Specification

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Specification)