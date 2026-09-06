from django.urls import path

from . import views


app_name = "consent"


urlpatterns = [

    path(
        "",
        views.consent_list,
        name="list",
    ),

    path(
        "<int:consent_id>/",
        views.consent_detail,
        name="detail",
    ),

    path(
        "<int:consent_id>/approve/",
        views.approve_consent,
        name="approve",
    ),

    path(
        "<int:consent_id>/reject/",
        views.reject_consent,
        name="reject",
    ),

    path(
        "<int:consent_id>/revoke/",
        views.revoke_consent,
        name="revoke",
    ),
]