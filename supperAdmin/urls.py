from django.urls import path

from .views import (
    DashboardInformation,
)

app_name = 'supperAdmin'

urlpatterns = [
    path('dashboardInformation/supperAdmin/', DashboardInformation.as_view(), name='dashboard_information_supperAdmin'),
]