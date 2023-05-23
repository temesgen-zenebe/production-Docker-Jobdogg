from django.urls import path
from .views import (
    DashboardInformation,
)

app_name = 'employer'

urlpatterns = [
    path('dashboardInformation/employer/', DashboardInformation.as_view(), name='dashboard_information_employer'),
]