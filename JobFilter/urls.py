from django.urls import path

from JobFilter.views import ApplyJobFromSearchView, FilteredJobListView


app_name = 'JobFilter'

urlpatterns = [
    path('jobFilter/', FilteredJobListView.as_view(), name='filtered-job-list'),
    path('jobFilter/ApplySearchJobView/<slug:slug>/apply/', ApplyJobFromSearchView.as_view(), name='apply-search-job'),
]