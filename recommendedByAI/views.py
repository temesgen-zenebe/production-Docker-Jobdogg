from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import RecommendedJobs

class RecommendedJobsListView(LoginRequiredMixin, ListView):
    model = RecommendedJobs
    template_name = 'AIrecommended/recommended_jobs_list.html'
    context_object_name = 'recommended_jobs'

class RecommendedJobsDetailView(LoginRequiredMixin,DetailView):
    model = RecommendedJobs
    template_name = 'AIrecommended/recommended_jobs_detail.html'
    context_object_name = 'recommended_job'

class RecommendedJobsDeleteView(LoginRequiredMixin,DeleteView):
    model = RecommendedJobs
    template_name = 'AIrecommended/recommended_jobs_confirm_delete.html'
    success_url = reverse_lazy('recommendedByAI:job-recommended-list')
    
    """
class RecommendedJobsCreateView(LoginRequiredMixin ,CreateView):
    model = RecommendedJobs
    fields = ['employee_preferences', 'job_requisition']
    template_name = 'recommended_jobs_form.html'

class RecommendedJobsUpdateView(LoginRequiredMixin,UpdateView):
    model = RecommendedJobs
    fields = ['employee_preferences', 'job_requisition']
    template_name = 'recommended_jobs_form.html'
    
    """