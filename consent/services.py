from django.utils import timezone

from .models import ConsentRequest


def has_valid_consent(
    citizen,
    departments=None,
    requested_data=None,
):
    """
    Check whether the citizen has an approved consent
    for the requested departments and data.
    """

    departments = departments or []
    requested_data = requested_data or []

    consent_requests = ConsentRequest.objects.filter(
        citizen=citizen,
        status="APPROVED",
    )

    now = timezone.now()

    for consent in consent_requests:

        # Check expiry
        if consent.expires_at and consent.expires_at < now:
            continue

        # Check departments
        consent_departments = set(
            consent.departments or []
        )

        if departments:
            if not set(departments).issubset(
                consent_departments
            ):
                continue

        # Check requested data
        consent_data = set(
            consent.requested_data or []
        )

        if requested_data:
            if not set(requested_data).issubset(
                consent_data
            ):
                continue

        # Check revocation
        try:
            record = consent.record

            if not record.granted:
                continue

            if record.revoked_at:
                continue

        except Exception:
            continue

        return True

    return False