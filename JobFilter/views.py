from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (TemplateView,ListView, CreateView,
                                  UpdateView, DetailView, DeleteView, FormView)
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from JobFilter.forms import JobFilterForm
from employer.models import CompanyProfile, JobRequisition
from JobFilter.models import AppliedSearchJobHistory
from django.db.models import Q


class FilteredJobListView(LoginRequiredMixin, TemplateView):
    template_name = 'JobFilter/jobFiltered/jobFiltered_list.html'
    paginate_by = 5  # Number of jobs per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = JobFilterForm(self.request.GET)
        applied_jobs = AppliedSearchJobHistory.objects.filter(user=self.request.user)
        
        # Filtered job queryset
        filtered_jobs = JobRequisition.objects.all()
        
        for job in filtered_jobs:
            job.company_profile = CompanyProfile.objects.filter(user=job.user).first()

        if form.is_valid():
            industry = form.cleaned_data['industry']
            job_title = form.cleaned_data['job_title']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            min_experience = form.cleaned_data['min_experience']
            job_type = form.cleaned_data.get('job_type')  # Get job_type from the form
            work_arrangement_preference = form.cleaned_data.get('work_arrangement_preference')  # Get work_arrangement_preference from the form

            if industry:
                filtered_jobs = filtered_jobs.filter(industry=industry)
            if job_title:
                filtered_jobs = filtered_jobs.filter(job_title=job_title)
            if city:
                filtered_jobs = filtered_jobs.filter(city__icontains=city)
            if state:
                filtered_jobs = filtered_jobs.filter(state__iexact=state)
            if min_experience:
                filtered_jobs = filtered_jobs.filter(min_experience__gte=min_experience)
            
            # Apply additional filters
            if job_type:
                filtered_jobs = filtered_jobs.filter(job_type=job_type)
            if work_arrangement_preference:
                filtered_jobs = filtered_jobs.filter(work_arrangement_preference=work_arrangement_preference)
                
            # Sorting
            sorting = form.cleaned_data.get('sorting')
            if sorting:
                if sorting == 'newest':
                    filtered_jobs = filtered_jobs.order_by('-created')
                    # Add more sorting options as needed
                    
            # Add search functionality using Q objects
            search = form.cleaned_data['search']
            if search:
                query = Q(
                    Q(job_description__icontains=search) |
                    Q(custom_job_title__icontains=search)
                    # Add more Q conditions as needed for other fields
                )
                filtered_jobs = filtered_jobs.filter(query) 

        paginator = Paginator(filtered_jobs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['jobs'] = page_obj
        context['form'] = form
        context['applied_jobs'] = applied_jobs

        return context

class FilteredJobDetailView(LoginRequiredMixin, DetailView):
    model = JobRequisition
    context_object_name = 'job' 
    template_name = 'JobFilter/jobFiltered/jobFiltered_detail.html'
    

class ApplyJobFromSearchView(LoginRequiredMixin, View):
    def post(self, request, slug):
        try:
            search_job = JobRequisition.objects.get(slug=slug)  # Retrieve the JobRequisition
            user = request.user

            # Check if the user has already applied for this job
            existing_application = AppliedSearchJobHistory.objects.filter(user=user, Search_job=search_job).first()

            if existing_application:
                messages.warning(request, "You have already applied for this job.")
            else:
                AppliedSearchJobHistory.objects.create(user=user, Search_job=search_job, status='applied')
                messages.success(request, "You have successfully applied for the job.")

        except JobRequisition.DoesNotExist:
            messages.error(request, "Job not found.")

        return redirect('JobFilter:filtered-job-list')  # Adjust the redirect URL accordingly
