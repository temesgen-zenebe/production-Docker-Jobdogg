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
    DashboardInformation,
    
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
    
)
app_name = 'employee' 

urlpatterns = [
    #-----policies-----------
    path('policies/list/', PolicyListView.as_view(), name='policies_list'),
    path('policies/accept/', AcceptPoliciesView.as_view(), name='accept_policies'),
    path('policies/<slug:slug>/', PoliciesDetailView.as_view(), name='policies_detail'),
    path('policies/accept/<slug:slug>/', PoliciesAcceptView.as_view(), name='policies_accept'),
    path('policies/create/', PoliciesCreateView.as_view(), name='policies_create'),
    path('policies/update/<slug:slug>/', PoliciesUpdateView.as_view(), name='policies_update'),
    path('policies/delete/<slug:slug>/', PoliciesDeleteView.as_view(), name='policies_delete'),
    path('dashboardInformation/employee', DashboardInformation.as_view(), name='dashboard_information_employee'),
    
    #----basic_information----
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
]





