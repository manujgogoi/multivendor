from django.core import validators
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from address.models import Address
from django.core.validators import RegexValidator


User = get_user_model()


# Create your models here.

class DeliveryAddress(models.Model):
    address = models.ForeignKey(Address, related_name="delivery_addresses", on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey('Profile', related_name="delivery_addresses", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('DeliveryAddress')
        verbose_name_plural = _('DeliveryAddresses')

    def __str__(self):
        return self.address.village_or_town.name

def upload_profile_photo_path(instance, filename):
    user_email = instance.user.email
    return f"user_profile/photos/{user_email}/{filename}"


class Profile(models.Model):
    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=30,
    )

    middle_name = models.CharField(
        verbose_name=_('Middle Name'),
        max_length=30,
        null=True,
        blank=True
    )

    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=30,
    )

    birthday = models.DateField(
        verbose_name=_("Birthday"),
        null=True,
        blank=True,
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
    )

    is_phone_verified = models.BooleanField(default=False)

    photo = models.ImageField(
        verbose_name=_('profile_photo'),
        help_text=_('Your profile photo'),
        upload_to=upload_profile_photo_path,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    address = models.OneToOneField(Address, related_name="user_profile", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['first_name']
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.first_name + ' ' + self.last_name