from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView,TemplateView,ListView
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
from employer.forms import CompanyProfileCreateForm
from employer.models import CompanyProfile,ProfileBuildingController

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
        
#----Profile Models ------
class ProfileBuildingProgressController(LoginRequiredMixin, View):
    template_name = 'employer/companyProfile/profileBuildingController.html'
    
    def get_progress_percentage_controller(self, profile):
        total_steps = 7  # Total number of steps in the profile
        completed_steps = sum(
            [
                profile.is_account_created,
                profile.is_company_profile_created,
                profile.is_payment_information_created,
                profile.is_police_accepted_created,
                profile.is_contract_signed_created,
                profile.is_payment_plan_validated,
                profile.is_billing_information_created,
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
        
