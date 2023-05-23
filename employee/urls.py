from django.urls import path
from .views import (
    PoliciesListView,
    PoliciesDetailView,
    PoliciesAcceptView,
    PoliciesCreateView,
    PoliciesUpdateView,
    PoliciesDeleteView,
    PolicyListView,
    AcceptPoliciesView,
)
app_name = 'employee' 

urlpatterns = [
    path('policies/list/', PolicyListView.as_view(), name='policies_list'),
    path('policies/accept/', AcceptPoliciesView.as_view(), name='accept_policies'),
    path('policies/<slug:slug>/', PoliciesDetailView.as_view(), name='policies_detail'),
    path('policies/accept/<slug:slug>/', PoliciesAcceptView.as_view(), name='policies_accept'),
    path('policies/create/', PoliciesCreateView.as_view(), name='policies_create'),
    path('policies/update/<slug:slug>/', PoliciesUpdateView.as_view(), name='policies_update'),
    path('policies/delete/<slug:slug>/', PoliciesDeleteView.as_view(), name='policies_delete'),
]




