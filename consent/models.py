from django.conf import settings
from django.db import models


class ConsentRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("EXPIRED", "Expired"),
    ]

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consent_requests",
    )

    purpose = models.CharField(
        max_length=255
    )

    requested_data = models.JSONField(
        default=list,
        blank=True
    )

    departments = models.JSONField(
        default=list,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    responded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-requested_at"]

    def __str__(self):
        return (
            f"Consent #{self.id} - "
            f"{self.citizen.username} - "
            f"{self.status}"
        )


class ConsentRecord(models.Model):

    consent_request = models.OneToOneField(
        ConsentRequest,
        on_delete=models.CASCADE,
        related_name="record",
    )

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consent_records",
    )

    granted = models.BooleanField(
        default=False
    )

    consent_text = models.TextField()

    granted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    revoked_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-granted_at"]

    def __str__(self):
        return (
            f"Consent Record #{self.id} - "
            f"{'Granted' if self.granted else 'Not Granted'}"
        )