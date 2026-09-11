from django.urls import path

from . import api_views


app_name = "interoperability"


urlpatterns = [

    # Simulated department APIs
    path(
        "revenue/citizen/",
        api_views.revenue_citizen_data,
        name="revenue-citizen-data",
    ),

    path(
        "education/citizen/",
        api_views.education_citizen_data,
        name="education-citizen-data",
    ),

    path(
        "health/citizen/",
        api_views.health_citizen_data,
        name="health-citizen-data",
    ),

    # SarvaHConn API Gateway
    path(
        "gateway/citizen/",
        api_views.gateway_citizen_data,
        name="gateway-citizen-data",
    ),

    # API health
    path(
        "health/",
        api_views.api_health,
        name="api-health",
    ),

    path(
        "gateway/health/",
        api_views.gateway_health_page,
        name="gateway-health",
    ),

    path(
    "external/citizen/",
    api_views.external_citizen_data,
    name="external-citizen-data",
    ),
]