from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.validators import UnicodeUsernameValidator

from accounts.models import User, Profile


class SettingsForm(forms.Form):
    username = forms.CharField(max_length=32, validators=[UnicodeUsernameValidator])
    email = forms.EmailField()


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
