from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    search_fields = ['email']
    form = UserAdminChangeForm  # Edit view
    add_form = UserAdminCreationForm # Create view

    list_display = ('email', 'admin')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'active', 'staff')}),
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
                'fields': ('active', 'staff', 'admin')
            }

        )
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()
    class Meta:
        model = User


admin.site.register(User, UserAdmin)
