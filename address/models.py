from django.db import models
from django.utils.translation import gettext as _

# State Model
class State(models.Model):
    name = models.CharField(
        verbose_name=_("State Name"),
        max_length=100,
        unique=True
    )
    is_deliverable = models.BooleanField(
        verbose_name=_("Is Deliverable"),
        help_text=_("Product deliverable or not"),        
        default=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return self.name
    

class District(models.Model):
    name = models.CharField(
        verbose_name=_("District Name"),
        max_length=100,
        unique=True
    )
    is_deliverable = models.BooleanField(
        verbose_name=_("Is Deliverable"),
        help_text=_("Product deliverable or not"),   
        default=True
    )
    state = models.ForeignKey(State, related_name="districts", on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    def __str__(self):
        return self.name

class PIN(models.Model):
    code = models.CharField(
        verbose_name=_("PIN code"),
        max_length=10,
    )
    is_deliverable = models.BooleanField(
        verbose_name=_("Is Deliverable"),
        help_text=_("Product deliverable or not"),   
        default=True
    )
    district = models.ForeignKey(District, related_name="pin_codes", on_delete=models.CASCADE)

    class Meta:
        ordering = ['code']
        verbose_name = 'PIN'
        verbose_name_plural = 'PINs'

    def __str__(self):
        return self.code

class VillageOrTown(models.Model):
    name = models.CharField(
        verbose_name=_("Village/Town Name"),
        max_length=100,
    )
    is_deliverable = models.BooleanField(
        verbose_name=_("Is Deliverable"),
        help_text=_("Product deliverable or not"),   
        default=True
    )
    pin = models.ForeignKey(PIN, related_name="villages_or_towns", on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'village/Town'
        verbose_name_plural = 'villages/Towns'

    def __str__(self):
        return self.name


class Address(models.Model):
    house_no = models.CharField(
        verbose_name=_("House No"),
        help_text=_("House No./ Door No./ Flat No./ Apartment No./ Qtr No."),
        max_length=50,
        null=True,
        blank=True
    )
    landmark = models.CharField(
        verbose_name=_("Landmark"),
        max_length=100,
    )
    village_or_town = models.ForeignKey(VillageOrTown, related_name="addresses", on_delete=models.RESTRICT)
