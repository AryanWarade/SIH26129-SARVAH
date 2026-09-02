from django.db import models


class Service(models.Model):

    class Category(models.TextChoices):
        CERTIFICATE = "CERTIFICATE", "Certificate"
        SCHOLARSHIP = "SCHOLARSHIP", "Scholarship"
        VERIFICATION = "VERIFICATION", "Verification"
        BENEFIT = "BENEFIT", "Benefit"
        ASSISTANCE = "ASSISTANCE", "Assistance"

    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        related_name="services",
    )

    name = models.CharField(
        max_length=200,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField()

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
    )

    eligibility = models.TextField(
        blank=True,
    )

    required_information = models.JSONField(
        default=list,
        blank=True,
    )

    processing_stages = models.JSONField(
        default=list,
        blank=True,
    )

    estimated_days = models.PositiveIntegerField(
        default=7,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_simulated = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["department__name", "name"]

    def __str__(self):
        return self.name