from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import RecommendedJobs
from django.views import View
from .models import RecommendedJobs, AppliedJobHistory
from common.utils.text import unique_slug

class RecommendedJobsListView(LoginRequiredMixin, ListView):
    model = RecommendedJobs
    template_name = 'AIrecommended/recommended_jobs_list.html'
    context_object_name = 'recommended_jobs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch AppliedJobHistory entries for the current user
        applied_jobs = AppliedJobHistory.objects.filter(user=self.request.user)
        
        context['applied_jobs'] = applied_jobs
        return context

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

class ApplyJobView(LoginRequiredMixin, View):

    def post(self, request, slug):
            recommended_job = RecommendedJobs.objects.get(slug=slug)
            
            # Check if the user has already applied for this job
            existing_application = AppliedJobHistory.objects.filter(user=request.user, job=recommended_job).first()
            
            if existing_application:
                pass #messages.warning(request, "You have already applied for this job.")
            else:
                AppliedJobHistory.objects.create(user=request.user, job=recommended_job, status='applied')
                #messages.success(request, "You have successfully applied for the job.")
            
            return redirect('recommendedByAI:job-recommended-detail', slug=slug)
