from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    # Sign Up Form
    first_name = forms.CharField(
        max_length=30, required=False, label=_('First name'), help_text=_('Enter your first name'))
    last_name = forms.CharField(
        max_length=30, required=False, label=_('Last name'), help_text=_('Enter your last name'))
    email = forms.EmailField(
        max_length=254, help_text=_('Enter a valid email address'))
    password1 = forms.CharField(
        max_length=30, label=_('Password'), widget=forms.PasswordInput, help_text=_('Your password must contain at least 8 characters. Can’t be too similar to your other personal information, commonly used password and entirely numeric.'))
    password2 = forms.CharField(
        max_length=30, label=_('Password confirmation'), widget=forms.PasswordInput, help_text=_('Enter the same password as before, for verification.'))

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]
