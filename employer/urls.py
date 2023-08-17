from django.urls import path

from .views import (
    #company-profile
    CompanyProfileDeleteView,
    CompanyProfileUpdateView,
    CompanyProfileCreateView,
    CompanyProfileListView,
    EmployerPolicyListView,
    
    #ProfileBuildingProgressController
    ProfileBuildingProgressController,
    
    DashboardInformation,
    BeEmployerRequestView, 
    #StartTrialView, 
    ActivateEmployerView,
    VilificationSandMassage,
)

app_name = 'employer'

urlpatterns = [
    path('employerProfileBuildingProgress/', ProfileBuildingProgressController.as_view(), name='profile_building_progress_controller'),
    # URL for the beEmployer request page
    path('dashboardInformation/be_employer/', BeEmployerRequestView.as_view(), name='be_employer_request'),
    path('dashboardInformation/be_employer/VilificationSandMassage/', VilificationSandMassage.as_view(), name='vilificationSandMassage'),
    # URL for activating the employer account
    path('dashboardInformation/activate_employer/', ActivateEmployerView.as_view(), name='activate_employer'), 
    path('dashboardInformation/employer/', DashboardInformation.as_view(), name='dashboard_information_employer'),
    
    path('company-policies/list/', EmployerPolicyListView.as_view(), name='company_policies_list'),
    #company-profile
    path('company-profile-list/', CompanyProfileListView.as_view(), name='company-profile-list'),
    path('company-profile/create/', CompanyProfileCreateView.as_view(), name='create-company-profile'),
    path('company-profile/<slug:slug>/update', CompanyProfileUpdateView.as_view(), name='company-profile-update'),
    path('company-profile/<slug:slug>/delete', CompanyProfileDeleteView.as_view(), name='company-profile-delete'),
]

