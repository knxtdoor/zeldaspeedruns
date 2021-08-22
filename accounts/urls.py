from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('manage/', views.SettingsView.as_view(), name='acm'),
    path('manage/profile/', views.ProfileSettingsView.as_view(), name='manage_profile'),
    path('manage/connections/', views.ConnectionsView.as_view(), name='connections'),
    path('manage/email_change/<str:code>/', views.EmailChangeView.as_view(), name='email_change'),
]
