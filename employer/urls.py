from django.urls import path

from .views import (
    DashboardInformation,
    BeEmployerRequestView, 
    #StartTrialView, 
    ActivateEmployerView,
    VilificationSandMassage,
)

app_name = 'employer'

urlpatterns = [
    
    # URL for the beEmployer request page
    path('dashboardInformation/be_employer/', BeEmployerRequestView.as_view(), name='be_employer_request'),
    path('dashboardInformation/be_employer/VilificationSandMassage/', VilificationSandMassage.as_view(), name='vilificationSandMassage'),
    # URL for activating the employer account
    path('dashboardInformation/activate_employer/', ActivateEmployerView.as_view(), name='activate_employer'),
     
    path('dashboardInformation/employer/', DashboardInformation.as_view(), name='dashboard_information_employer'),
]

