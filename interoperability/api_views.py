import time

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from departments.models import Department

from .adapters import DepartmentAPIAdapter
from .models import APITransaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from consent.services import has_valid_consent





@api_view(["GET"])
@permission_classes([AllowAny])
def revenue_citizen_data(request):

    citizen_code = request.GET.get(
        "citizen_code",
        "MH1001",
    )

    data = {
        "citizen_code": citizen_code,
        "full_name": "Demo Citizen",
        "income_value": 250000,
        "residence": "Pune",
    }

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def education_citizen_data(request):

    student_id = request.GET.get(
        "student_id",
        "EDU5501",
    )

    data = {
        "student_id": student_id,
        "student_name": "Demo Citizen",
        "course": "B.Tech",
        "institution": "Demo Institute",
    }

    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_citizen_data(request):

    patient_ref = request.GET.get(
        "patient_ref",
        "HLT8801",
    )

    data = {
        "patient_ref": patient_ref,
        "name": "Demo Citizen",
        "scheme_status": "Eligible",
    }

    return Response(data)


@api_view(["GET"])
def gateway_citizen_data(request):

    if not request.user.is_authenticated:
        return Response(
            {
                "success": False,
                "message": "Authentication required.",
            },
            status=401,
        )

    citizen_code = request.GET.get(
        "citizen_code",
        "MH1001",
    )

    required_departments = [
        "EDUCATION",
        "REVENUE",
        "HEALTH",
    ]

    required_data = [
        "Full Name",
    ]

    if not has_valid_consent(
        request.user,
        departments=required_departments,
        requested_data=required_data,
    ):
        return Response(
            {
                "success": False,
                "message": (
                    "Approved consent is required "
                    "before retrieving department data."
                ),
            },
            status=403,
        )

    start_time = time.perf_counter()

    result = {}

    try:

        revenue = DepartmentAPIAdapter.get_revenue_data(
            citizen_code
        )

        education = DepartmentAPIAdapter.get_education_data(
            "EDU5501"
        )

        health = DepartmentAPIAdapter.get_health_data(
            "HLT8801"
        )

        result = {
            "master_citizen_id": "MHC-1001",

            "full_name": "Demo Citizen",

            "revenue": revenue,

            "education": education,

            "health": health,

            "verified": True,

            "message": (
                "Citizen data successfully retrieved "
                "with valid consent."
            ),
        }

        response_time = int(
            (time.perf_counter() - start_time) * 1000
        )

        APITransaction.objects.create(
            operation="GET_CITIZEN_DATA",
            endpoint="/api/interoperability/gateway/citizen/",
            request_data={
                "citizen_code": citizen_code,
            },
            response_data=result,
            http_status=200,
            status="SUCCESS",
            response_time_ms=response_time,
        )

        return Response(result)

    except Exception as e:

        response_time = int(
            (time.perf_counter() - start_time) * 1000
        )

        APITransaction.objects.create(
            operation="GET_CITIZEN_DATA",
            endpoint="/api/interoperability/gateway/citizen/",
            request_data={
                "citizen_code": citizen_code,
            },
            response_data={},
            http_status=500,
            status="FAILED",
            error_message=str(e),
            response_time_ms=response_time,
        )

        return Response(
            {
                "success": False,
                "message": "Unable to retrieve department data.",
                "error": str(e),
            },
            status=500,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def api_health(request):

    departments = [
        (
            "REVENUE",
            "Revenue Department",
            "/api/interoperability/revenue/citizen/",
        ),
        (
            "EDUCATION",
            "Education Department",
            "/api/interoperability/education/citizen/",
        ),
        (
            "HEALTH",
            "Health Department",
            "/api/interoperability/health/citizen/",
        ),
    ]

    results = []

    for code, name, endpoint in departments:

        start_time = time.perf_counter()

        try:

            if code == "REVENUE":

                DepartmentAPIAdapter.get_revenue_data(
                    "MH1001"
                )

            elif code == "EDUCATION":

                DepartmentAPIAdapter.get_education_data(
                    "EDU5501"
                )

            elif code == "HEALTH":

                DepartmentAPIAdapter.get_health_data(
                    "HLT8801"
                )

            response_time = int(
                (time.perf_counter() - start_time) * 1000
            )

            results.append(
                {
                    "department": name,
                    "code": code,
                    "status": "ONLINE",
                    "response_time_ms": response_time,
                    "endpoint": endpoint,
                }
            )

        except Exception as e:

            response_time = int(
                (time.perf_counter() - start_time) * 1000
            )

            results.append(
                {
                    "department": name,
                    "code": code,
                    "status": "OFFLINE",
                    "response_time_ms": response_time,
                    "endpoint": endpoint,
                    "error": str(e),
                }
            )

    return Response(
        {
            "success": True,
            "services": results,
        }
    )


def gateway_health_page(request):

    return JsonResponse(
        {
            "service": "SarvaHConn API Gateway",
            "status": "Operational",
        }
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def data_gov_resource(request):

    resource_id = request.GET.get("resource_id")

    if not resource_id:
        return Response(
            {
                "success": False,
                "message": "resource_id is required."
            },
            status=400,
        )

    try:

        data = ExternalAPIService.fetch_data_gov_resource(
            resource_id=resource_id,
            limit=10,
        )

        return Response(data)

    except Exception as e:

        return Response(
            {
                "success": False,
                "message": "Unable to retrieve data from data.gov.in.",
                "error": str(e),
            },
            status=500,
        )

@api_view(["GET"])
@permission_classes([AllowAny])
def external_citizen_data(request):
    """
    Simulated external government system API.

    This intentionally uses a different schema from
    SARVAH's internal citizen data.
    """

    external_id = request.GET.get(
        "external_id",
        "EXT-1001"
    )

    data = {
        "external_id": external_id,
        "name": "Demo Citizen",
        "district_name": "Pune",
        "annual_income": 250000,
        "verification_status": "VERIFIED",
    }

    return Response(data)