from . import views
from django.urls import path
from .views import (
    #-------Policies------
    PoliciesListView,
    PoliciesDetailView,
    PoliciesAcceptView,
    PoliciesCreateView,
    PoliciesUpdateView,
    PoliciesDeleteView,
    PolicyListView,
    AcceptPoliciesView,
    
    #
    DashboardInformation,
    ProfileBuildingProgress,
    
    #----BasicInformation----
    BasicInformationListView,
    BasicInformationCreateView,
    BasicInformationDetailView,
    BasicInformationUpdateView,
    BasicInformationDeleteView,
    
    #----PERSONAL-------
    PersonalCreateView,
    PersonalDeleteView,
    PersonalDetailView,
    PersonalListView,
    PersonalUpdateView,
    
    #----- Military----
    MilitaryCreateView,
    MilitaryUpdateView,
    MilitaryDetailView,
    MilitaryListView,
    MilitaryDeleteView,
    SkipMilitaryView,
    
    #Education
    EducationListView,
    EducationCreateView,
    EducationDetailView,
    EducationUpdateView,
    EducationDeleteView,
    
    #Certification&License
    CertificationLicenseListView,
    CertificationLicenseCreateView,
    CertificationLicenseUpdateView,
    CertificationLicenseDeleteView,
    CertificationLicenseDetailView,
    
    #Experience
    ExperienceDeleteView,
    ExperienceDetailView,
    ExperienceListView,
    ExperienceUpdateView,
    ExperienceCreateView,
    
    #No ExperienceView 
    NoExperienceView,
    PositionsView,
    SkillsView,
     
    #Preferences
    EmployeePreferencesListView,
    EmployeePreferencesCreateView,
    EmployeePreferencesUpdateView,
    EmployeePreferencesDetailView,
    EmployeePreferencesDeleteView,
    
    #SkipSkillSetTestView
    SkipSkillSetTestView,
)
from employee import views
app_name = 'employee' 

urlpatterns = [
    
    # DashboardInformation Employee
    path('dashboardInformation/employee', DashboardInformation.as_view(), name='dashboard_information_employee'),
    path('profileBuildingProgress/', ProfileBuildingProgress.as_view(), name='profile_building_progress'),
    #skip Military
    path('skipMilitary/', SkipMilitaryView.as_view(), name='skip_military'),
    #No ExperienceView 
    path('no_Experience/', NoExperienceView.as_view(), name='no_Experience'),
    #Positions
    path('positions/', PositionsView.as_view(), name='positions'),
    path('skills/', SkillsView.as_view(), name='skills'),
    #-----policies-----------
    path('policies/list/', PolicyListView.as_view(), name='policies_list'),
    path('policies/accept/', AcceptPoliciesView.as_view(), name='accept_policies'),
    path('policies/<slug:slug>/', PoliciesDetailView.as_view(), name='policies_detail'),
    path('policies/accept/<slug:slug>/', PoliciesAcceptView.as_view(), name='policies_accept'),
    
    #----admin managing policies by admin----
    path('policies/create/', PoliciesCreateView.as_view(), name='policies_create'),
    path('policies/update/<slug:slug>/', PoliciesUpdateView.as_view(), name='policies_update'),
    path('policies/delete/<slug:slug>/', PoliciesDeleteView.as_view(), name='policies_delete'),
    
    # basic_information
    path('basic_information/list/', BasicInformationListView.as_view(), name='basic_information_list'),
    path('basic_information/create/', BasicInformationCreateView.as_view(), name='basic_information_create'),
    path('basic_information/update/<slug:slug>/', BasicInformationUpdateView.as_view(), name='basic_information_update'),
    path('basic_information/detail/<slug:slug>/', BasicInformationDetailView.as_view(), name='basic_information_detail'),
    path('basic_information/delete/<slug:slug>/', BasicInformationDeleteView.as_view(), name='basic_information_delete'),

    # personal
    path('personal/list/', PersonalListView.as_view(), name='personal_list'),
    path('personal/detail/<slug:slug>/', PersonalDetailView.as_view(), name='personal_detail'),
    path('personal/create/', PersonalCreateView.as_view(), name='personal_create'),
    path('personal/update/<slug:slug>/', PersonalUpdateView.as_view(), name='personal_update'),
    path('personal/delete/<slug:slug>/', PersonalDeleteView.as_view(), name='personal_delete'),

    #  Military
    path('military/list/', MilitaryListView.as_view(), name='military_list'),
    path('military/create/', MilitaryCreateView.as_view(), name='military_create'),
    path('military/<slug:slug>/', MilitaryDetailView.as_view(), name='military_detail'),
    path('military/<slug:slug>/update/', MilitaryUpdateView.as_view(), name='military_update'),
    path('military/<slug:slug>/delete/', MilitaryDeleteView.as_view(), name='military_delete'),
    
    #Education
    path('education/list/', EducationListView.as_view(), name='education_list'),
    path('education/create/',EducationCreateView.as_view(), name='education_create'),
    path('education/<slug:slug>/', EducationDetailView.as_view(), name='education_detail'),
    path('education/<slug:slug>/update/', EducationUpdateView.as_view(), name='education_update'),
    path('education/<slug:slug>/delete/', EducationDeleteView.as_view(), name='education_delete'),
    
   # Certification License URLs
    path('certification-licenses/', CertificationLicenseListView.as_view(), name='certification_license_list'),
    path('certification-licenses/create/', CertificationLicenseCreateView.as_view(), name='certification_license_create'),
    path('certification-licenses/<int:pk>/update/', CertificationLicenseUpdateView.as_view(), name='certification_license_update'),
    path('certification-licenses/<int:pk>/delete/', CertificationLicenseDeleteView.as_view(), name='certification_license_delete'),
    path('certification-licenses/<int:pk>/', CertificationLicenseDetailView.as_view(), name='certification_license_detail'),
 
    #Experience
    path('experience/list/', ExperienceListView.as_view(), name='experience_list'),
    path('experience/create/',ExperienceCreateView.as_view(), name='experience_create'),
    path('experience/<slug:slug>/', ExperienceDetailView.as_view(), name='experience_detail'),
    path('experience/<slug:slug>/update/', ExperienceUpdateView.as_view(), name='experience_update'),
    path('experience/<slug:slug>/delete/', ExperienceDeleteView.as_view(), name='experience_delete'),
    
    #Preferences 
    path('preferences/', EmployeePreferencesListView.as_view(), name='employee-preferences-list'),
    path('preferences/create/', EmployeePreferencesCreateView.as_view(), name='employee-preferences-create'),
    path('preferences/<slug:slug>/', EmployeePreferencesDetailView.as_view(), name='employee-preferences-detail'),
    path('preferences/<slug:slug>/update/', EmployeePreferencesUpdateView.as_view(), name='employee-preferences-update'),
    path('preferences/<slug:slug>/delete/', EmployeePreferencesDeleteView.as_view(), name='employee-preferences-delete'),
    
    #SkipSkillSetTestView
     path('skipSkillSetTestView/', SkipSkillSetTestView.as_view(), name='SkipSkillSetTestView'),
]




