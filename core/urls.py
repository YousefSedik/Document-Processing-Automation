from django.urls import path
from .api import DashboardAPIView

app_name = "core"
urlpatterns = [
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
]
