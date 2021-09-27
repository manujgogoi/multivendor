from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_superuser="False"):
        if not email:
            raise ValueError(_("Users must have an email address"))
        if not password:
            raise ValueError(_("Users must have a password"))

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.is_active      = is_active
        user_obj.is_staff       = is_staff
        user_obj.is_superuser   = is_superuser
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True, is_superuser=True)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(_('email id'), max_length=255, unique=True)
    is_active       = models.BooleanField(_('is active'), default=True) # Can login
    is_staff        = models.BooleanField(_('staff status'), default=False) # Staff user non Super
    is_superuser    = models.BooleanField(_('is superuser'), default=False) # Superuser
    date_joined     = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = [] # USERNAME_FIELD and password are required by default


    objects = UserManager()


    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
