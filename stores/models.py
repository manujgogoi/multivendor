from enum import auto
from django.db import models
from django.utils.translation import gettext as _

from mptt.models import MPTTModel, TreeForeignKey

from vendor.models import Vendor


MAX_DIGITS = 10
DECIMAL_PLACES = 2

# Product category model
class Category(MPTTModel):
    title = models.CharField(
        verbose_name=_("Category title"),
        max_length=50, 
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Is Active"),
        help_text=_("Change category visibility"),
        default=True)
    parent = TreeForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        ordering = ('title', )
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


# Product model
class Product(models.Model):
    title = models.CharField(
        verbose_name=_("Product title"),
        max_length=100
    )
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(
        verbose_name=_("SKU"),
        help_text=_("Stock Keeping Unit"),
        max_length=15, 
        blank=True, 
        null=True
    )
    regular_price = models.DecimalField(
        verbose_name=_("Regular price"),
        help_text=_("Maximum 99999999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 99999999.99"),
            },
        },
        max_digits=MAX_DIGITS, 
        decimal_places=DECIMAL_PLACES
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Maximum 99999999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 99999999.99"),
            },
        },
        max_digits=MAX_DIGITS, 
        decimal_places=DECIMAL_PLACES, 
        blank=True, 
        null=True
    )
    wholesale_price = models.DecimalField(
        verbose_name=_("Wholesale price"),
        help_text=_("Maximum 99999999.99"),
        error_messages={
            "name": {
                "max_length": _("The price must be between 0 and 99999999.99"),
            },
        },
        max_digits=MAX_DIGITS, 
        decimal_places=DECIMAL_PLACES, 
        blank=True, 
        null=True
    )
    quantity = models.IntegerField(blank=True, null=True)
    wholesale_min_quantity = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True
    )
    is_featured = models.BooleanField(
        verbose_name=_("Featured product"),
        help_text=_("Mark as featured product"),
        default=False)
    is_downloadable = models.BooleanField(
        help_text=_("Mark as downloadable product"),
        default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    # image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    # thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails 

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


# Image uploading path   
def upload_image_path(instance, filename):
    product_dir = instance.product.title.replace(" ", "_")
    product_dir += '_' + str(instance.product.id)
    return f"stores/images/{product_dir}/{filename}"


class Image(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to=upload_image_path
    )
    alt_text = models.CharField(max_length=100, blank=True, null=True)
    is_featured = models.BooleanField(
        verbose_name=_("Featured image"),
        help_text=_("Mark as featured image"),
        default=False
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return str(self.image.name)


class Specification(models.Model):
    product = models.ForeignKey(Product, related_name="specifications", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name = 'Specification'
        verbose_name_plural = 'Specifications'

    def __str__(self):
        return self.name + ':' + self.value