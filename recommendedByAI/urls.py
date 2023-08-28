#recommendedByAI

from django.urls import path
from .views import (
    ApplyJobView,
    RecommendedJobsListView,
    RecommendedJobsDetailView,
    #RecommendedJobsCreateView,
    #RecommendedJobsUpdateView,
    RecommendedJobsDeleteView,
)

app_name = 'recommendedByAI' 

urlpatterns = [
    path('AiRecommended/', RecommendedJobsListView.as_view(), name='job-recommended-list'),
    path('AiRecommended/<slug:slug>/', RecommendedJobsDetailView.as_view(), name='job-recommended-detail'),
    #path('AiRecommended/create/', RecommendedJobsCreateView.as_view(), name='job-create'),
    #path('AiRecommended/<slug:slug>/update/', RecommendedJobsUpdateView.as_view(), name='job-update'),
    path('AiRecommended/<slug:slug>/delete/', RecommendedJobsDeleteView.as_view(), name='job-recommended-delete'),
    path('ApplyJobView/<slug:slug>/apply/', ApplyJobView.as_view(), name='apply-job'),
   
]
