from django.urls import path

from JobFilter.views import ApplyJobFromSearchView, FilteredJobListView, FilteredJobDetailView


app_name = 'JobFilter'

urlpatterns = [
    path('jobFilter/', FilteredJobListView.as_view(), name='filtered-job-list'),
    path('jobFilter/ApplySearchJobView/<slug:slug>/apply/', ApplyJobFromSearchView.as_view(), name='apply-search-job'),
    path('jobFilter/<slug:slug>/detail/', FilteredJobDetailView.as_view(), name='job_jobFilter_detail'),
]