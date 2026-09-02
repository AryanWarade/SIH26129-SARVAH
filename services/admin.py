from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "department",
        "category",
        "estimated_days",
        "is_active",
        "is_simulated",
    )

    list_filter = (
        "department",
        "category",
        "is_active",
        "is_simulated",
    )

    search_fields = (
        "name",
        "code",
        "description",
    )