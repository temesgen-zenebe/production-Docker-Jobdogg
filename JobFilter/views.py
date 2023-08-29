from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (TemplateView,ListView, CreateView,
                                  UpdateView, DetailView, DeleteView, FormView)
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from JobFilter.forms import JobFilterForm
from employer.models import JobRequisition
from JobFilter.models import AppliedSearchJobHistory



class FilteredJobListView(TemplateView):
    template_name = 'JobFilter/jobFiltered/jobFiltered_list.html'
    paginate_by = 5  # Number of jobs per page


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = JobFilterForm(self.request.GET)
        filtered_jobs = JobRequisition.objects.all()
        # Fetch AppliedJobHistory entries for the current user
        applied_jobs = AppliedSearchJobHistory.objects.filter(user=self.request.user)

        if form.is_valid():
            industry = form.cleaned_data['industry']
            job_title = form.cleaned_data['job_title']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            min_experience = form.cleaned_data['min_experience']
            # Process other form fields to filter jobs

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
            # Apply more filters

        paginator = Paginator(filtered_jobs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['jobs'] = page_obj
        context['form'] = form
        context['applied_jobs'] = applied_jobs
        return context

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
