from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_demo_user",
    )

    list_filter = (
        "role",
        "is_active",
        "is_demo_user",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "SarvaHConn Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "is_demo_user",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "SarvaHConn Information",
            {
                "fields": (
                    "email",
                    "role",
                    "phone",
                    "is_demo_user",
                )
            },
        ),
    )