from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView,TemplateView,ListView, DetailView

# Your other imports
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.models import Group
from django.conf import settings
import stripe
import paypalrestsdk
from common.utils.email import send_email
from django.core.mail import send_mail
import uuid
from employee.models import Position, Skill
from employer.forms import CompanyProfileCreateForm, JobRequisitionForm 
from employer.models import(
    CompanyProfile,
    EmployerAcceptedPolicies, 
    EmployerPoliciesAndTerms,
    ProfileBuildingController, 
    JobRequisition,
    
)

User = settings.AUTH_USER_MODEL

class DashboardInformation(LoginRequiredMixin, View):
    template_name = 'employer/dashboardInfo.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
   
class BeEmployerRequestView(LoginRequiredMixin, View):
    
    
    def get(self, request):
        context = {}
        return render(request, 'employer/be_employer_request.html', context)
    
    def post(self, request):
        
        # Send email request to the system using SendGrid
        activation_key = str(uuid.uuid4())  # Generate a unique activation key
        activation_link = request.build_absolute_uri(reverse('employer:activate_employer')) 

        message = f"Click the following link to activate your employer account:\n{activation_link}"
        send_mail(
            subject='Activate Your Employer Account',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        return redirect('employer:vilificationSandMassage')
         
class ActivateEmployerView(LoginRequiredMixin, View):
    def get(self, request):
        # Update user group to "is_employer" and activate the account
        user = request.user
        current_group = user.groups.first()
        employer_group = Group.objects.get(name='employer')
        employee_group = Group.objects.get(name='employee')

        if  current_group and current_group.name == 'employee':
            user.groups.remove(current_group)
            user.groups.add(employer_group)
            user.is_active = True
            user.save()
        else :
            user.groups.add(employer_group)
            user.is_active = True
            user.save()
           
        return redirect('employer:dashboard_information_employer')  # Replace 'dashboard' with the actual URL name of the user's dashboard

class VilificationSandMassage(TemplateView):
    template_name = 'employer/verification.html'  
#----Profile Models ------
class ProfileBuildingProgressController(LoginRequiredMixin, View):
    template_name = 'employer/companyProfile/profileBuildingController.html'
    
    def get_progress_percentage_controller(self, profile):
        total_steps = 4  # Total number of steps in the profile
        completed_steps = sum(
            [
                profile.is_account_created,
                profile.is_company_profile_created,
                profile.is_payment_information_created,
                profile.is_police_accepted_created,
                #profile.is_contract_signed_created,
                #profile.is_payment_plan_validated,
                #profile.is_billing_information_created,
            ]
        )
        progress_percentage = (completed_steps / total_steps) * 100
        return int(progress_percentage)
 
    
    def get(self, request):
        try:
            profile = ProfileBuildingController.objects.get(user=request.user)
            progress_percentage = self.get_progress_percentage_controller(profile)
            userProfileProgress = profile
            
        except ProfileBuildingController.DoesNotExist:
            # If the profile doesn't exist, create it
            profile = ProfileBuildingController.objects.create(user=request.user)
            userProfileProgress = get_object_or_404(ProfileBuildingController, user=request.user)
            progress_percentage = self.get_progress_percentage_controller(userProfileProgress)
          

        context = {
            'progress': userProfileProgress,
            'progress_percentage': progress_percentage,      
        }

        return render(request, self.template_name, context)

#CompanyProfile CRUD
class CompanyProfileListView(LoginRequiredMixin, ListView):
    model = CompanyProfile
    template_name = 'employer/companyProfile/company_profile_list.html'  # Use your actual template name
    context_object_name = 'company_profiles'
    
    def get_queryset(self):
        return CompanyProfile.objects.filter(user=self.request.user)
   
class CompanyProfileCreateView(LoginRequiredMixin, CreateView):
    model = CompanyProfile
    form_class = CompanyProfileCreateForm
    template_name = 'employer/companyProfile/company_profile_create.html'  # Use your actual template name
    success_url = reverse_lazy('employer:company-profile-list')  # Replace with your actual success URL
  
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            BuildingController = ProfileBuildingController.objects.get(user=request.user)
        except BuildingController.DoesNotExist:
            BuildingController = ProfileBuildingController(user=request.user)
            
        if not BuildingController.is_account_created:
            BuildingController.is_account_created = True
            
        BuildingController.is_company_profile_created= True
        BuildingController.save()
        
        return super().dispatch(request, *args, **kwargs)
    
class CompanyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CompanyProfile
    form_class = CompanyProfileCreateForm
    template_name = 'employer/companyProfile/company_profile_update.html'
    success_url = reverse_lazy('employer:company-profile-list')

class CompanyProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CompanyProfile
    template_name = 'employer/companyProfile/company_profile_delete.html'
    success_url = reverse_lazy('employer:company-profile-list')
    
    def dispatch(self, request, *args, **kwargs):
        try:
            BuildingController = ProfileBuildingController.objects.get(user=request.user)
        except BuildingController.DoesNotExist:
            BuildingController = ProfileBuildingController(user=request.user)
               
        BuildingController.is_company_profile_created= False
        BuildingController.save()
        
        return super().dispatch(request, *args, **kwargs)
        
class EmployerPolicyListView(LoginRequiredMixin, View):
    template_name = 'employer/policy/policy_list.html'
    context_object_name = 'policies'
    acceptedAll = False
    
    def get(self, request):
        policies = EmployerPoliciesAndTerms.objects.all()
        accepted_policies = EmployerAcceptedPolicies.objects.filter(user=request.user)
        accepted_policies_ids = [policy.policies_id for policy in accepted_policies]
        total_policies_count = policies.count()
        accepted_policies_count = len(accepted_policies_ids)
        all_policies_accepted = accepted_policies_count == total_policies_count

        context = {
             self.context_object_name: policies,
            'accepted_policies':accepted_policies,
            'accepted_policies_ids': accepted_policies_ids,
            'all_policies_accepted': all_policies_accepted,
        }
       
        return render(request, self.template_name, context)
        

    def post(self, request):
        
        policies = EmployerPoliciesAndTerms.objects.all()
        accepted_policies = []

        for policy in policies:
            accepted = request.POST.get(f'policy_{policy.id}')
            if accepted == 'on':
                accepted_policies.append(EmployerAcceptedPolicies(user=request.user, policies=policy, accepted=True))

        EmployerAcceptedPolicies.objects.bulk_create(accepted_policies)
        
        # Retrieve the user's profile
        
        accepted_policies = EmployerAcceptedPolicies.objects.filter(user=request.user)
        accepted_policies_ids = [policy.policies_id for policy in accepted_policies]
        total_policies_count = policies.count()
        accepted_policies_count = len(accepted_policies_ids)
        all_policies_accepted = accepted_policies_count == total_policies_count
        
        if all_policies_accepted == True:
            # Retrieve the user's profile
            profile, created = ProfileBuildingController.objects.get_or_create(user=request.user)
            #profile = Profile.objects.get(user=request.user)
            
            # Update the  companyPolices_completed field to True
            profile.is_police_accepted_created = True
            profile.save()
            
        # Update is_accepted context states to True    
        request.session['is_accepted'] = True

        messages.success(request, 'Policies accepted successfully.')
        return redirect('employer:profile_building_progress_controller')       



#job_title View and Dynamic dropdown views
class JobTitleView(View):
    def get(self, request):
        industry_id = request.GET.get('industry_Id')
        #print(industry_id)
        job_titles = Position.objects.filter(category_id=industry_id).values('id', 'position')
        #print(list(job_titles))
        return JsonResponse({'job_titles': list(job_titles)})
    
#requiredSkills View
class RequiredSkillsView(View):
    def get(self, request):
        position_id = request.GET.get('positionId')
        skills = Skill.objects.filter(position__id=position_id)
        skills_data = [{'id': skill.id, 'skill': skill.skill} for skill in skills]
        return JsonResponse({'skills': skills_data})
    

#JobRequisition
class JobRequisitionListView(LoginRequiredMixin, ListView):
    model = JobRequisition
    template_name = 'employer/jobRequisition/job_requisition_list.html'
    context_object_name = 'job_requisitions'

class JobRequisitionDetailView(LoginRequiredMixin, DetailView):
    model = JobRequisition
    template_name = 'employer/jobRequisition/job_requisition_detail.html'
    context_object_name = 'job_requisition'

class JobRequisitionCreateView(LoginRequiredMixin, CreateView):
    model = JobRequisition
    form_class = JobRequisitionForm
    template_name = 'employer/jobRequisition/job_requisition_create.html'
    success_url = reverse_lazy('employer:job_requisition_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.industry_id = form.cleaned_data['industry'].id  # Assign the category ID
        
        # Save the instance to the database
        self.object = form.save()
        
        # Get the selected positions and skills from the form data
        job_title = self.request.POST.getlist('job_title')
        required_skills = self.request.POST.getlist('required_skills')

        # Set the many-to-many relationships
        self.object.job_title.set(job_title)
        self.object.required_skills.set(required_skills)

        return super().form_valid(form)
    
class JobRequisitionUpdateView(LoginRequiredMixin, UpdateView):
    model = JobRequisition
    form_class = JobRequisitionForm
    template_name = 'employer/jobRequisition/job_requisition_update.html'
    success_url = reverse_lazy('employer:job_requisition_list')


class JobRequisitionDeleteView(LoginRequiredMixin, DeleteView):
    model = JobRequisition
    success_url = reverse_lazy('employer:job_requisition_list')
    template_name = 'employer/jobRequisition/job_requisition_confirm_delete.html'



