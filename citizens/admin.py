from django.contrib import admin

from .models import CitizenProfile


@admin.register(CitizenProfile)
class CitizenProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "district",
        "state",
        "profile_verified",
        "created_at",
    )

    list_filter = (
        "profile_verified",
        "state",
        "district",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )