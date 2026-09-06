from django.contrib import admin

from .models import ConsentRequest, ConsentRecord


@admin.register(ConsentRequest)
class ConsentRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "citizen",
        "purpose",
        "status",
        "requested_at",
        "expires_at",
    )

    list_filter = (
        "status",
        "requested_at",
    )

    search_fields = (
        "citizen__username",
        "citizen__email",
        "purpose",
    )


@admin.register(ConsentRecord)
class ConsentRecordAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "citizen",
        "granted",
        "granted_at",
        "revoked_at",
    )

    list_filter = (
        "granted",
        "granted_at",
    )

    search_fields = (
        "citizen__username",
        "citizen__email",
    )