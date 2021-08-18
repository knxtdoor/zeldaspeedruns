from django.urls import path

from accounts.views import SettingsView, ConnectionsView

app_name = 'accounts'
urlpatterns = [
    path('manage/', SettingsView.as_view(), name='acm'),
    path('manage/connections/', ConnectionsView.as_view(), name='connections'),
]
