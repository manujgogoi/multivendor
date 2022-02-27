from django.db import models
from django.utils.translation import gettext as _
from accounts.models import User
from address.models import VillageOrTown


def upload_id_proof_document_path(instance, filename):
    user_email = instance.user.email
    return f"courier/id_proof/{user_email}/{filename}"

def upload_address_proof_document_path(instance, filename):
    user_email = instance.user.email
    return f"courier/address_proof/{user_email}/{filename}"


class Carrier(models.Model):

    # Constants
    PAN = 'PN'
    AADHAAR = 'AD'
    PASSPORT = 'PP'
    DRIVING_LICENSE = 'DL'
    BANK_PASSBOOK = 'BP'
    
    # ID proof types
    ID_PROOF_TYPES = (
        (PAN, 'PAN Card'),
        (AADHAAR, 'Aadhaar Card'),
        (PASSPORT, 'Passport'),
        (DRIVING_LICENSE, 'Driving License'),
    )

    # Address proof types
    ADDRESS_PROOF_TYPES = (
        (AADHAAR, 'Aadhaar Card'),
        (PASSPORT, 'Passport'),
        (BANK_PASSBOOK, 'Bank Passbook'),
    )


    user = models.ForeignKey(
        User, 
        related_name="carriers", 
        on_delete=models.CASCADE
    )
    
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=50,
    )
    middle_name = models.CharField(
        verbose_name=_("Middle Name"),
        max_length=50,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=50,
    )
    house_no = models.CharField(
        verbose_name=_('House No'),
        max_length=20,
        null=True,
        blank=True,
    )
    landmark = models.CharField(
        verbose_name=_('Landmark'),
        max_length=50,
        null=True,
        blank=True,
    )
    vill_or_town = models.CharField(
        verbose_name=_('Village / Town'),
        max_length=50,
        null=True,
        blank=True,
    )
    district = models.CharField(
        verbose_name=_('District'),
        max_length=50,
        null=True,
        blank=True,
    )
    state = models.CharField(
        verbose_name=_('State'),
        max_length=50,
        null=True,
        blank=True,
    )
    country = models.CharField(
        verbose_name=_('Country'),
        max_length=50,
        null=True,
        blank=True,
    )
    pin_code = models.CharField(
        verbose_name=_('PIN Code'),
        max_length=10,
        null=True,
        blank=True,
    )
    mobile_no = models.CharField(
        verbose_name=_('Mobile No'),
        max_length=15,
        null=True,
        blank=True
    )
    mobile_verified = models.BooleanField(
        verbose_name=_('Is mobile verified'),
        default=False
    )
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        default=True
    )
    id_proof_type = models.CharField(max_length=2, choices=ID_PROOF_TYPES)
    id_proof_number = models.CharField(max_length=25, unique=True, null=True, blank=True)
    id_proof_document = models.ImageField(
        verbose_name=_('id proof document'),
        help_text=_('Id proof document'),
        upload_to=upload_id_proof_document_path,
        null=True,
        blank=True,
    )
    address_proof_document = models.ImageField(
        verbose_name=_('address proof document'),
        help_text=_('Address proof document'),
        upload_to=upload_address_proof_document_path,
        null=True,
        blank=True,
    )
    address_proof_type = models.CharField(max_length=2, choices=ADDRESS_PROOF_TYPES)
    address_proof_number = models.CharField(max_length=25, unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['first_name']
        verbose_name='Carrier'
        verbose_name_plural = 'Carriers'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class ServiceArea(models.Model):
    carrier = models.ForeignKey(Carrier, related_name="service_areas", null=True, blank=True, on_delete=models.CASCADE)
    vill_or_town = models.ForeignKey(VillageOrTown, related_name="service_areas", null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
