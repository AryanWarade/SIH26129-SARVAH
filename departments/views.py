from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import User


@login_required
def officer_dashboard(request):

    if request.user.role != User.Role.OFFICER:
        return render(
            request,
            "public/access_denied.html",
            status=403,
        )

    return render(
        request,
        "officer/dashboard.html",
    )