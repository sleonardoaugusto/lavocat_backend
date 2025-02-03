from django.contrib import admin

from backend.core.models import UserAllowed


@admin.register(UserAllowed)
class UserAllowedAdmin(admin.ModelAdmin):
    pass
