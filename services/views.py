from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Service


@login_required
def service_list(request):

    services = Service.objects.filter(
        is_active=True
    ).select_related("department")

    department = request.GET.get("department")
    category = request.GET.get("category")
    search = request.GET.get("search", "").strip()

    if department:
        services = services.filter(
            department__code=department
        )

    if category:
        services = services.filter(
            category=category
        )

    if search:
        services = services.filter(
            name__icontains=search
        )

    return render(
        request,
        "services/service_list.html",
        {
            "services": services,
            "search": search,
            "selected_department": department,
            "selected_category": category,
        },
    )


@login_required
def service_detail(request, service_id):

    service = get_object_or_404(
        Service.objects.select_related("department"),
        id=service_id,
        is_active=True,
    )

    return render(
        request,
        "services/service_detail.html",
        {
            "service": service,
        },
    )