from django.core import validators
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from address.models import State, District, PIN, VillageOrTown
from django.core.validators import RegexValidator


User = get_user_model()


# Create your models here.

class DeliveryAddress(models.Model):
    # address = models.ForeignKey(Address, related_name="delivery_addresses", on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey('Profile', related_name="delivery_addresses", on_delete=models.CASCADE)
    state = models.ForeignKey(State, related_name="delivery_addresses", on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, related_name="delivery_addresses", on_delete=models.SET_NULL, null=True, blank=True)
    pin_code = models.ForeignKey(PIN, related_name="delivery_addresses", on_delete=models.SET_NULL, null=True, blank=True)
    village_or_town = models.ForeignKey(VillageOrTown, related_name="delivery_addresses", on_delete=models.SET_NULL, null=True, blank=True)
    house_no = models.CharField(
        verbose_name=_('house_no'),
        help_text=_('House no./ Quarter no./ Building no/ Apartment Name ...'),
        max_length=50,
    )
    landmark = models.CharField(
        verbose_name=_('landmark'),
        help_text=_('Road name/ Nearby building/ Office ...'),
        max_length=50,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('DeliveryAddress')
        verbose_name_plural = _('DeliveryAddresses')

    def __str__(self):
        return self.village_or_town.name

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

    phone_regex = RegexValidator(
        regex=r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$', 
        message="Example 18005551234, +91 800 555 1234 etc."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True
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
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    state = models.ForeignKey(State, related_name="user_profiles", on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, related_name="user_profiles", on_delete=models.SET_NULL, null=True, blank=True)
    pin_code = models.ForeignKey(PIN, related_name="user_profiles", on_delete=models.SET_NULL, null=True, blank=True)
    village_or_town = models.ForeignKey(VillageOrTown, related_name="user_profiles", on_delete=models.SET_NULL, null=True, blank=True)
    house_no = models.CharField(
        verbose_name=_('house_no'),
        help_text=_('House no./ Quarter no./ Building no/ Apartment Name ...'),
        max_length=50
    )
    landmark = models.CharField(
        verbose_name=_('landmark'),
        help_text=_('Road name/ Nearby building/ Office ...'),
        max_length=50,
    )


    class Meta:
        ordering = ['first_name']
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.first_name + ' ' + self.last_name