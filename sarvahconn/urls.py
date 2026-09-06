from django.contrib import admin
from django.urls import include, path

from accounts import views


urlpatterns = [

    path(
        "django-admin/",
        admin.site.urls,
    ),

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "",
        include("accounts.urls"),
    ),

    path("citizen/", include("citizens.urls")),

    path(
        "services/",
        include("services.urls"),
    ),

    path(
        "api/interoperability/",
        include("interoperability.api_urls"),
    ),

    path(
    "consent/",
    include("consent.urls"),
    ),
    
]