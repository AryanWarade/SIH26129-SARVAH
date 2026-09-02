from django.contrib import admin

from .models import Department , DepartmentUser


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "head_officer",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

@admin.register(DepartmentUser)
class DepartmentUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "department",
        "designation",
        "employee_code",
        "is_active",
    )

    list_filter = (
        "department",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__email",
        "employee_code",
    )