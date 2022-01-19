import uuid
from django.db import models
from stores.models import Product
from accounts.models import User
from vendor.models import Vendor
from user_profile.models import DeliveryAddress


MAX_DIGITS = 10
DECIMAL_PLACES = 2

# Create your models here.

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(
        DeliveryAddress, 
        related_name='orders', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    quantity = models.IntegerField(default=1)
    discount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        blank=True, 
        null=True
    )
    total = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
#     price = models.DecimalField(
#         max_digits=MAX_DIGITS, 
#         decimal_places=DECIMAL_PLACES
#     )
#     quantity = models.IntegerField(default=1)
#     discount = models.DecimalField(
#         max_digits=MAX_DIGITS,
#         decimal_places=DECIMAL_PLACES
#     )
#     total = models.DecimalField(
#         max_digits=MAX_DIGITS,
#         decimal_places=DECIMAL_PLACES
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)