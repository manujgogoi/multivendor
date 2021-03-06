from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(
                        _("vendor name"),
                        validators=[
                            MinLengthValidator(3, message=_("Minimum 3 Characters Long"))
                        ], 
                        max_length=255)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name