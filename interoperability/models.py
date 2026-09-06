from django.db import models


class MasterCitizen(models.Model):

    master_citizen_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    full_name = models.CharField(
        max_length=200,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    district = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        default="Maharashtra",
    )

    is_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["master_citizen_id"]

    def __str__(self):
        return self.master_citizen_id


class DepartmentIdentity(models.Model):

    master_citizen = models.ForeignKey(
        MasterCitizen,
        on_delete=models.CASCADE,
        related_name="department_identities",
    )

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="citizen_identities",
    )

    department_reference = models.CharField(
        max_length=100,
    )

    source_name = models.CharField(
        max_length=150,
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    last_verified_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "department",
                    "department_reference",
                ],
                name="unique_department_reference",
            )
        ]

    def __str__(self):
        return (
            f"{self.department.code} - "
            f"{self.department_reference}"
        )


class IdentityMapping(models.Model):

    master_citizen = models.ForeignKey(
        MasterCitizen,
        on_delete=models.CASCADE,
        related_name="identity_mappings",
    )

    department_identity = models.ForeignKey(
        DepartmentIdentity,
        on_delete=models.CASCADE,
        related_name="mappings",
    )

    match_method = models.CharField(
        max_length=100,
        default="Verified profile match",
    )

    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.master_citizen.master_citizen_id} → "
            f"{self.department_identity.department_reference}"
        )

class APITransaction(models.Model):

    STATUS_CHOICES = [
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="api_transactions",
    )

    operation = models.CharField(
        max_length=100,
    )

    endpoint = models.CharField(
        max_length=255,
    )

    request_data = models.JSONField(
        default=dict,
        blank=True,
    )

    response_data = models.JSONField(
        default=dict,
        blank=True,
    )

    http_status = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SUCCESS",
    )

    error_message = models.TextField(
        blank=True,
    )

    response_time_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.operation} - "
            f"{self.status} - "
            f"{self.created_at}"
        )