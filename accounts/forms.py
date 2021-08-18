from django import forms


class SettingsForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=32,
    )
    email = forms.EmailField(
        label='Email address',
    )
