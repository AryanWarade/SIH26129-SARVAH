from django.urls import path
from . import views

app_name = "citizens"

urlpatterns = [
    path("dashboard/", views.dashboard, name="citizen_dashboard"),
]