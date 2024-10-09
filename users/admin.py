from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("username", "is_superuser", "is_active", )
    list_display = ("pk", "username", "email", "is_superuser", "is_active", "last_login")
    ordering = ["username", "is_superuser"]

