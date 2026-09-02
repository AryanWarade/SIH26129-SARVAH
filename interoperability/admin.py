from django.contrib import admin

from .models import (
    DepartmentIdentity,
    IdentityMapping,
    MasterCitizen,
)


@admin.register(MasterCitizen)
class MasterCitizenAdmin(admin.ModelAdmin):

    list_display = (
        "master_citizen_id",
        "full_name",
        "district",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "is_verified",
        "state",
        "district",
    )

    search_fields = (
        "master_citizen_id",
        "full_name",
        "email",
        "phone",
    )


@admin.register(DepartmentIdentity)
class DepartmentIdentityAdmin(admin.ModelAdmin):

    list_display = (
        "master_citizen",
        "department",
        "department_reference",
        "is_verified",
        "last_verified_at",
    )

    list_filter = (
        "department",
        "is_verified",
    )

    search_fields = (
        "department_reference",
        "master_citizen__master_citizen_id",
        "master_citizen__full_name",
    )


@admin.register(IdentityMapping)
class IdentityMappingAdmin(admin.ModelAdmin):

    list_display = (
        "master_citizen",
        "department_identity",
        "match_method",
        "confidence_score",
        "is_verified",
    )

    list_filter = (
        "is_verified",
        "match_method",
    )