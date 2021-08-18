from django.urls import path

from accounts.views import SettingsView

app_name = 'accounts'
urlpatterns = [
    path('manage/', SettingsView.as_view(), name='acm')
]
