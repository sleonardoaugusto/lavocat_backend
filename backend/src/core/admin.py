from django.contrib import admin

from src.core.models import UserAllowed


@admin.register(UserAllowed)
class UserAllowedAdmin(admin.ModelAdmin):
    pass
