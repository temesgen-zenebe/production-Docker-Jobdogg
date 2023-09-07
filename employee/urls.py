from . import views
from django.urls import path
from employee import views
from .views import (
    
    #RidePreference
   
    RidePreferenceCreateView,
    RidePreferenceDetailView,
    RidePreferenceListView,
    RidePreferenceUpdateView,
    RidePreferenceDeleteView,
    
    #--Policies------
    PoliciesListView,
    PoliciesDetailView,
    PoliciesAcceptView,
    PoliciesCreateView,
    PoliciesUpdateView,
    PoliciesDeleteView,
    PolicyListView,
    AcceptPoliciesView,
    
    #Dashboard
    DashboardInformation,
    ProfileBuildingProgress,
    
    #--BasicInformation----
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
    SkillsTestComingSoon,
     
    #Preferences
    EmployeePreferencesListView,
    EmployeePreferencesCreateView,
    EmployeePreferencesUpdateView,
    EmployeePreferencesDetailView,
    EmployeePreferencesDeleteView,
    
    #SkipSkillSetTestView
    SkipSkillSetTestView,
    OnProgressSkillTestView,
    GenerateSkillTestView,
    
    #SkillSetTestResultList
    SkillSetTestResultListView, 
    SkillSetTestResultCreateView, 
    SkillSetTestResultUpdateView, 
    SkillSetTestResultDeleteView,
    SkillSetTestResultDetailView,
    
    #SafetyVideoTest
    SafetyVideoTestListView,
    SafetyVideoTestDetailView,
    SafetyVideoTestCreateView,
    SafetyVideoTestUpdateView,
    SafetyVideoTestDeleteView,
    
    #VideoResume
    VideoResumeListView,
    VideoResumeCreateView,
    VideoResumeUpdateView,
    VideoResumeDeleteView,
    VideoResumeDetailView,
    
    #BackgroundCheckCreateView
    BackgroundCheckListView,
    BackgroundCheckCreateView,
    BackgroundCheckUpdateView,
    BackgroundCheckDeleteView,
    BackgroundCheckDetailView,
    
    #CheckByEmail
    CheckByEmailListView,
    CheckByEmailDetailView,
    CheckByEmailCreateView,
    CheckByEmailUpdateView,
    CheckByEmailDeleteView,
   
)


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
    path('testComingSoon/', SkillsTestComingSoon.as_view(), name='testComingSoon'),
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
    path('OnProgress/', OnProgressSkillTestView.as_view(), name='OnProgressSetTest'),
    path('generateMyTest/', GenerateSkillTestView.as_view(), name='generate_test'),
    
    #SkillSetTestResultList 
    path('skillsettestresult/', SkillSetTestResultListView.as_view(), name='skillsettestresult-list'),
    path('skillsettestresult/create/', SkillSetTestResultCreateView.as_view(), name='skillsettestresult-create'),
    path('skillsettestresult/<slug:slug>/', SkillSetTestResultDetailView.as_view(), name='skillsettestresult-detail'),

    path('skillsettestresult/<slug:slug>/update/', SkillSetTestResultUpdateView.as_view(), name='skillsettestresult-update'),
    path('skillsettestresult/<slug:slug>/delete/', SkillSetTestResultDeleteView.as_view(), name='skillsettestresult-delete'),
    

    #SafetyVideoTest
    path('safety-video-test/', SafetyVideoTestListView.as_view(), name='safetyVideoTest_list'),
    path('safety-video-test/create/', SafetyVideoTestCreateView.as_view(), name='safetyVideoTest_create'),
    path('safety-video-test/<int:pk>/', SafetyVideoTestDetailView.as_view(), name='safetyVideoTest_detail'),
    path('safety-video-test/<int:pk>/update/', SafetyVideoTestUpdateView.as_view(), name='safetyVideoTest_update'),
    path('safety-video-test/<int:pk>/delete/', SafetyVideoTestDeleteView.as_view(), name='safetyVideoTest_delete'),

    #VideoResume
    path('video-resumes/', VideoResumeListView.as_view(), name='video_resume_list'),
    path('video-resumes/create/', VideoResumeCreateView.as_view(), name='video_resume_create'),
    path('video-resumes/<slug:slug>/', VideoResumeDetailView.as_view(), name='video_resume_detail'),
    path('video-resumes/<slug:slug>/update/', VideoResumeUpdateView.as_view(), name='video_resume_update'),
    path('video-resumes/<slug:slug>/delete/', VideoResumeDeleteView.as_view(), name='video_resume_delete'),
    
    #background_check
    path('backgroundCheck/', BackgroundCheckListView.as_view(), name='background_check_list'),
    path('backgroundCheck/create/', BackgroundCheckCreateView.as_view(), name='background_check_create'),
    path('backgroundCheck/<slug:slug>/', BackgroundCheckDetailView.as_view(), name='background_check_detail'),
    path('backgroundCheck/<slug:slug>/update/', BackgroundCheckUpdateView.as_view(), name='background_check_update'),
    path('backgroundCheck/<slug:slug>/delete/', BackgroundCheckDeleteView.as_view(), name='background_check_delete'),

    #CheckByEmail
    path('checkByEmail/', CheckByEmailListView.as_view(), name='check_by_email_list'),
    path('checkByEmail/create/', CheckByEmailCreateView.as_view(), name='check_by_email_create'),
    path('checkByEmail/<slug:slug>/', CheckByEmailDetailView.as_view(), name='check_by_email_detail'),
    path('checkByEmail/<slug:slug>/update/', CheckByEmailUpdateView.as_view(), name='check_by_email_update'),
    path('checkByEmail/<slug:slug>/delete/', CheckByEmailDeleteView.as_view(), name='check_by_email_delete'),
    
    #EWallet
    path('eWallet/', views.EWalletListView.as_view(), name='e_wallet_list'),
    path('eWallet/create/', views.EWalletCreateView.as_view(), name='e_wallet_create'),
    path('eWallet/<slug:slug>/', views.EWalletDetailView.as_view(), name='e_wallet_detail'),
    path('eWallet/<slug:slug>/update/', views.EWalletUpdateView.as_view(), name='e_wallet_update'),
    path('eWallet/<slug:slug>/delete/', views.EWalletDeleteView.as_view(), name='e_wallet_delete'),
    
    #Card
    path('card/', views.CardListView.as_view(), name='card_list'),
    path('card/create/', views.CardCreateView.as_view(), name='card_create'),
    path('card/<slug:slug>/', views.CardDetailView.as_view(), name='card_detail'),
    path('card/<slug:slug>/update/', views.CardUpdateView.as_view(), name='card_update'),
    path('card/<slug:slug>/delete/', views.CardDeleteView.as_view(), name='card_delete'),
    
    # BankAccount 
    path('bankAccount/', views.BankAccountListView.as_view(), name='bankAccount_list'),
    path('bankAccount/create/', views.BankAccountCreateView.as_view(), name='bankAccount_create'),
    path('bankAccount/<slug:slug>/', views.BankAccountDetailView.as_view(), name='bankAccount_detail'),
    path('bankAccount/<slug:slug>/update/', views.BankAccountUpdateView.as_view(), name='bankAccount_update'),
    path('bankAccount/<slug:slug>/delete/', views.BankAccountDeleteView.as_view(), name='bankAccount_delete'),
    
    #RidePreference
    path('ride_preferences/', RidePreferenceListView.as_view(), name='ridePreference_list'),
    path('ride_preferences/create/', RidePreferenceCreateView.as_view(), name='ridePreference_create'),
    path('ride_preferences/<slug:slug>/', RidePreferenceDetailView.as_view(), name='ridePreference_detail'),
   
    path('ride_preferences/<slug:slug>/update/', RidePreferenceUpdateView.as_view(), name='ridePreference_update'),
    path('ride_preferences/<slug:slug>/delete/', RidePreferenceDeleteView.as_view(), name='ridePreference_delete'),

    #taxDocumentSetting
    path('taxDocumentSetting/', views.TaxDocumentSettingListView.as_view(), name='tax_document_setting_list'),
    path('taxDocumentSetting/create/', views.TaxDocumentSettingCreateView.as_view(), name='tax_document_setting_create'),
    path('taxDocumentSetting/<slug:slug>/', views.TaxDocumentSettingDetailView.as_view(), name='tax_document_setting_detail'),
    path('taxDocumentSetting/<slug:slug>/update/', views.TaxDocumentSettingUpdateView.as_view(), name='tax_document_setting_update'),
    path('taxDocumentSetting/<slug:slug>/delete/', views.TaxDocumentSettingDeleteView.as_view(), name='tax_document_setting_delete'),
    
]
