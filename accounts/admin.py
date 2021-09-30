from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):

    # Override get_form method to customize user permissions in Admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: set[str]

        if not is_superuser:
            disabled_fields |= {
                'is_superuser',
                'user_permissions',
            }

        # Prevent non-superusers from editing their own permissions
        # Prevent non-superusers from editing superuser permissions
        if (
            not is_superuser
            and obj is not None
            and (
                obj.is_superuser == True
                or obj == request.user
            )
        ):
            disabled_fields |= {
                'is_active',
                'is_staff',
                'is_superuser',
                'user_permissions'
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form



    search_fields = ['email']
    readonly_fields = ('date_joined', )
    
    form = UserAdminChangeForm  # Edit view
    add_form = UserAdminCreationForm # Create view

    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
        (
            "Permissions", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')
            }

        )
    )
    search_fields = ['email']
    ordering = ['date_joined']
    class Meta:
        model = User


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
