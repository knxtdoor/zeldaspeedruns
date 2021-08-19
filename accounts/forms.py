from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator


class SettingsForm(forms.Form):
    error_css_class = 'acm-form__row--error'

    username = forms.CharField(max_length=32, validators=[UnicodeUsernameValidator])
    email = forms.EmailField()
