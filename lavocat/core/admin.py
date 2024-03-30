from django.contrib import admin

from lavocat.core.models import UserAllowed


@admin.register(UserAllowed)
class UserAllowedAdmin(admin.ModelAdmin):
    pass
