from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "id": "user-password",
        }
    ))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(username__iexact=email)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid email")

        return email


class RegisterForm(forms.ModelForm):
    '''The Default'''
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={
            "class": "form-control", 
            "id": "user-password"
        }
    ))
    password2 = forms.CharField(label=_('Comfirm Password'), widget=forms.PasswordInput(
                attrs={
            "class": "form-control", 
            "id": "user-confirm-password"
        }
    ))

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''Verify email is available'''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError(_("email is taken"))
        return email

    def clean(self):
        '''Verify both passwords match'''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    '''
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    '''
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password Confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        '''Check that the two password entries match'''
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        '''Save the provided password in hashed format'''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    '''A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's 
    password hash display field.'''

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']

    def clean_password(self):
        '''Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the field 
        does not have access to the initial value'''
        return self.initial['password']