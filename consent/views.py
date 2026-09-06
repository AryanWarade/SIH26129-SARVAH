from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import ConsentRecord, ConsentRequest


@login_required
def consent_list(request):

    consent_requests = ConsentRequest.objects.filter(
        citizen=request.user
    )

    return render(
        request,
        "consent/list.html",
        {
            "consent_requests": consent_requests,
        },
    )


@login_required
def consent_detail(request, consent_id):

    consent_request = get_object_or_404(
        ConsentRequest,
        id=consent_id,
        citizen=request.user,
    )

    return render(
        request,
        "consent/detail.html",
        {
            "consent_request": consent_request,
        },
    )


@login_required
def approve_consent(request, consent_id):

    if request.method != "POST":
        return redirect(
            "consent:detail",
            consent_id=consent_id,
        )

    consent_request = get_object_or_404(
        ConsentRequest,
        id=consent_id,
        citizen=request.user,
    )

    if consent_request.status != "PENDING":
        messages.warning(
            request,
            "This consent request has already been processed.",
        )

        return redirect(
            "consent:detail",
            consent_id=consent_id,
        )

    consent_request.status = "APPROVED"
    consent_request.responded_at = timezone.now()
    consent_request.save(
        update_fields=[
            "status",
            "responded_at",
        ]
    )

    ConsentRecord.objects.update_or_create(
        consent_request=consent_request,
        defaults={
            "citizen": request.user,
            "granted": True,
            "consent_text": (
                "Citizen approved sharing the requested "
                "information for the stated purpose."
            ),
            "granted_at": timezone.now(),
            "revoked_at": None,
        },
    )

    messages.success(
        request,
        "Consent approved successfully.",
    )

    return redirect(
        "consent:detail",
        consent_id=consent_id,
    )


@login_required
def reject_consent(request, consent_id):

    if request.method != "POST":
        return redirect(
            "consent:detail",
            consent_id=consent_id,
        )

    consent_request = get_object_or_404(
        ConsentRequest,
        id=consent_id,
        citizen=request.user,
    )

    if consent_request.status != "PENDING":
        messages.warning(
            request,
            "This consent request has already been processed.",
        )

        return redirect(
            "consent:detail",
            consent_id=consent_id,
        )

    consent_request.status = "REJECTED"
    consent_request.responded_at = timezone.now()
    consent_request.save(
        update_fields=[
            "status",
            "responded_at",
        ]
    )

    ConsentRecord.objects.update_or_create(
        consent_request=consent_request,
        defaults={
            "citizen": request.user,
            "granted": False,
            "consent_text": (
                "Citizen rejected sharing the requested "
                "information."
            ),
            "granted_at": None,
            "revoked_at": None,
        },
    )

    messages.info(
        request,
        "Consent request rejected.",
    )

    return redirect(
        "consent:detail",
        consent_id=consent_id,
    )


@login_required
def revoke_consent(request, consent_id):

    if request.method != "POST":
        return redirect(
            "consent:detail",
            consent_id=consent_id,
        )

    consent_request = get_object_or_404(
        ConsentRequest,
        id=consent_id,
        citizen=request.user,
    )

    try:
        record = consent_request.record
    except ConsentRecord.DoesNotExist:
        messages.warning(
            request,
            "No active consent record was found.",
        )

        return redirect(
            "consent:detail",
            consent_id=consent_id,
        )

    record.granted = False
    record.revoked_at = timezone.now()
    record.save(
        update_fields=[
            "granted",
            "revoked_at",
        ]
    )

    consent_request.status = "REJECTED"
    consent_request.save(
        update_fields=["status"]
    )

    messages.success(
        request,
        "Consent has been revoked.",
    )

    return redirect(
        "consent:detail",
        consent_id=consent_id,
    )