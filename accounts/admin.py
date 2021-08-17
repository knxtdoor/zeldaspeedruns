from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (*BaseUserAdmin.fieldsets, ('Personalization', {'fields': ('avatar',)}))


admin.site.register(User, UserAdmin)
