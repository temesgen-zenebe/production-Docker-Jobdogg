from typing import Any
from urllib import response
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
from django.template import Library
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from employee.templatetags.mask_ssn import mask_ssn
from django.forms import CheckboxSelectMultiple
from django.views import View
from django.db.models import Q
import pandas as pd
import pyxlsb
import openpyxl
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
)

from .models import (
    Category,CertificationLicense,Education,EmployeePreferences,Experience, 
    Policies,Position,Profile,Skill, SkillSetTestResult,UserAcceptedPolicies,BasicInformation,
    Personal,Language,Military,
)
from .forms import (
    BasicInformationForm,
    CertificationLicenseForm,
    EducationForm,
    EmployeePreferencesForm,
    ExperienceForm,
    MilitaryForm,
    PersonalForm,
    ExperienceForm,
    MilitaryForm,
    PersonalForm,
    BasicInformationForm,
    UserAcceptedPoliciesForm
)


#----Policies Models ------
class DashboardInformation(LoginRequiredMixin, View):
    template_name = 'employee/dashboardInfo.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    
#----Policies Models ------
class ProfileBuildingProgress(LoginRequiredMixin, View):
    template_name = 'employee/profileBuildingProgress.html'
    
    def get_progress_percentage(self, profile):
        total_steps = 10  # Total number of steps in the profile
        completed_steps = sum(
            [
                profile.account_created,
                profile.companyPolices_completed,
                profile.basic_information_completed,
                profile.personal_information_completed,
                profile.Military_completed,
                profile.Education_completed,
                profile.Experience_completed,
                profile.Preferences_completed,
                profile.SkillSetTest_completed,
                profile.VideoResume_completed,
                profile.ResumeUploading_completed,
            ]
        )
        progress_percentage = (completed_steps / total_steps) * 100
        return int(progress_percentage)
    
    def get(self, request):
        # Retrieve all policies from the database
        policies = Policies.objects.all()
        accepted_policies = UserAcceptedPolicies.objects.filter(user=request.user)
        accepted_policies_ids = [policy.policies_id for policy in accepted_policies]
        total_policies_count = policies.count()
        accepted_policies_count = len(accepted_policies_ids)
        all_policies_accepted = accepted_policies_count == total_policies_count
        basic_information_form = BasicInformationForm()
        personal_form = PersonalForm()
        military_form = MilitaryForm()
        education_form = EducationForm()
        experienceForm_form = ExperienceForm()
        CertificationLicense_form = CertificationLicenseForm()
        # Retrieve all Certification License objects related to the user's Education
        certification_licenses = CertificationLicense.objects.filter(education__user=request.user)
        employee_preferences_form = EmployeePreferencesForm()
        progress = Profile.objects.filter(user=request.user)
        profile = get_object_or_404(Profile, user=request.user)
        progress_percentage = self.get_progress_percentage(profile)
        categories = Category.objects.all()
        positions = Position.objects.all()
        skills = Skill.objects.all()
        testList = SkillSetTestResult.objects.filter(user=self.request.user)
        # Filter positions based on the logged-in user's preferences
        employee_preferences = EmployeePreferences.objects.filter(user=self.request.user).first()
        if employee_preferences:
            user_positions = Position.objects.filter(category=employee_preferences.category)
        else: 
            user_positions = []
        context = {
            'basic_information_form': basic_information_form,
            'personal_form': personal_form,
            'military_form':military_form,
            'education_form': education_form,
            'CertificationLicense_form':CertificationLicense_form,
            'experienceForm_form':experienceForm_form,
            'employee_preferences_form':employee_preferences_form,
            'progress':progress,
            'progress_percentage': progress_percentage,
            'policies': policies,
            'accepted_policies_ids': accepted_policies_ids,
            'all_policies_accepted': all_policies_accepted,
            'certification_licenses':certification_licenses,
            'documents_uploaded': True,  # Set the flag to True if there are uploaded documents
            'categories': categories,
            'positions': positions,
            'skills': skills,
            'user_positions':user_positions,
            'testList':testList,
            
        }
           
        return render(request, self.template_name, context)
    
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)  # Retrieve the Profile object
        
        if 'policies' in request.POST:
            policies = Policies.objects.all()
            accepted_policies = []

            for policy in policies:
                accepted = request.POST.get(f'policy_{policy.id}')
                if accepted == 'on':
                    accepted_policies.append(UserAcceptedPolicies(user=request.user, policies=policy, accepted=True))

            UserAcceptedPolicies.objects.bulk_create(accepted_policies)
        
            # Retrieve the user's profile
            
            accepted_policies = UserAcceptedPolicies.objects.filter(user=request.user)
            accepted_policies_ids = [policy.policies_id for policy in accepted_policies]
            total_policies_count = policies.count()
            accepted_policies_count = len(accepted_policies_ids)
            all_policies_accepted = accepted_policies_count == total_policies_count
            
            if all_policies_accepted == True:
                # Retrieve the user's profile
                profile, created = Profile.objects.get_or_create(user=request.user)
                # Update the  companyPolices_completed field to True
                profile.companyPolices_completed = True
                profile.save()
                
            # Update is_accepted context states to True    
            request.session['is_accepted'] = True

            messages.success(request, 'Policies accepted successfully.')
            
            return redirect('employee:profile_building_progress')
            
        elif 'basic_information' in request.POST:
            basic_information_form = BasicInformationForm(request.POST)
            if basic_information_form.is_valid():
                basic_information = basic_information_form.save(commit=False)
                basic_information.user = request.user
                basic_information.save()
                profile.basic_information_completed = True  # Mark the step as completed in the profile
                profile.save()
                return redirect('employee:profile_building_progress')

        elif 'personal' in request.POST:
            personal_form = PersonalForm(request.POST)
            if personal_form.is_valid():
                personal = personal_form.save(commit=False)
                personal.user = request.user
                personal.save()
                profile.personal_information_completed = True  # Mark the step as completed in the profile
                profile.save()
                return redirect('employee:profile_building_progress')
            
        elif 'military' in request.POST:
            military_form = MilitaryForm(request.POST, request.FILES)
            
            if military_form.is_valid():
                military = military_form.save(commit=False)
                military.user = request.user
                military.save()
                profile.Military_completed = True  # Mark the step as completed in the profile
                profile.save()
                return redirect('employee:profile_building_progress')
        
        elif 'education' in request.POST:
            education_form = EducationForm(request.POST)
            
            if education_form.is_valid():
               education = education_form.save(commit=False)
               education.user = request.user
               education.save()
                # Update the corresponding profile completion field if needed
               profile.Education_completed = True
               profile.save()
               return redirect('employee:profile_building_progress')
        
        elif 'certificationLicense' in request.POST:
             form = CertificationLicenseForm(request.POST, request.FILES)
             if form.is_valid():
                certification_license = form.save(commit=False)
                education = Education.objects.filter(user=self.request.user).first()
                #print("Education object retrieved:", education)
                certification_license.education = education
                certification_license.save()
                return redirect('employee:profile_building_progress')
             else:
                print("Certification License form is invalid")
                
        elif 'experience' in request.POST:
            experience_form = ExperienceForm(request.POST)
            if experience_form.is_valid():
               experience = experience_form.save(commit=False)
               experience.user = request.user
               experience.save()
               # Update the corresponding profile completion field if needed
               profile.Experience_completed = True
               profile.save()
               return redirect('employee:profile_building_progress')
            else:
              print("Certification License form is invalid")
              
        elif 'preferences' in request.POST:
                employee_preferences_form = EmployeePreferencesForm(request.POST)
                if employee_preferences_form.is_valid():
                    employee_preferences = employee_preferences_form.save(commit=False)
                    employee_preferences.category_id = request.POST.get('category')  # Set the category ID from the form data
                    employee_preferences.user = request.user
                    employee_preferences.save()  # Save the EmployeePreferences instance
                    # Get the selected positions and skills from the form data
                    desired_positions = request.POST.getlist('desired_positions')
                    skills = request.POST.getlist('skills')

                    # Clear existing desired_positions and skills and set the new values
                    employee_preferences.desired_positions.clear()
                    employee_preferences.skills.clear()
                    employee_preferences.desired_positions.set(desired_positions)
                    employee_preferences.skills.set(skills)
                    
                    profile.Preferences_completed = True
                    profile.save()
                    return redirect('employee:profile_building_progress')
                else:
                    print(employee_preferences_form.errors)  # Print form errors

                
        else:
            pass   
        # If neither form was submitted or form validation failed, render the template again with the forms
        basic_information_form = BasicInformationForm()
        personal_form = PersonalForm()
        military_form = MilitaryForm()
        education_form = EducationForm()
        CertificationLicense_form = CertificationLicenseForm()
        experienceForm_form = ExperienceForm()
        employee_preferences_form = EmployeePreferencesForm()
       
        context = {
            'basic_information_form': basic_information_form,
            'personal_form': personal_form,
            'military_form':military_form,
            'education_form':education_form,
            'CertificationLicense_form':CertificationLicense_form,
            'experienceForm_form':experienceForm_form,
            'employee_preferences_form': employee_preferences_form
        }
        return render(request, self.template_name, context)
    
#skip military 
class SkipMilitaryView(LoginRequiredMixin, View):
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.Military_completed = True
        profile.save()
        messages.success(request, 'Military step skipped successfully.')
        return redirect('employee:profile_building_progress')
    
#skip Skip SkillSet Test
class SkipSkillSetTestView(LoginRequiredMixin, View):
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.Skipped_completed = True
        profile.SkillSetTest_completed = False
        profile.OnProgressSkillTest_completed=False
        profile.save()
        messages.success(request, 'Skip SkillSet Test step skipped successfully.')
        return redirect('employee:profile_building_progress')
    
class OnProgressSkillTestView(LoginRequiredMixin, View):
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.OnProgressSkillTest_completed = True
        profile.Skipped_completed = False
        profile.SkillSetTest_completed = False
        profile.save()
        messages.success(request, 'Skip SkillSet OnPrecess successfully.')
        return redirect('employee:profile_building_progress')  

#Positions View and Dynamic dropdown views
class PositionsView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        positions = Position.objects.filter(category_id=category_id).values('id', 'position')
        return JsonResponse({'positions': list(positions)})
    
#Skills View
class SkillsView(View):
    def get(self, request):
        position_id = request.GET.get('position_id')
        skills = Skill.objects.filter(position__id=position_id)
        skills_data = [{'id': skill.id, 'skill': skill.skill} for skill in skills]
        return JsonResponse({'skills': skills_data})
    
class PolicyListView(LoginRequiredMixin, View):
    template_name = 'employee/policy_list.html'
    context_object_name = 'policies'
    acceptedAll = False
    def get(self, request):
        policies = Policies.objects.all()
        accepted_policies = UserAcceptedPolicies.objects.filter(user=request.user)
        accepted_policies_ids = [policy.policies_id for policy in accepted_policies]
        total_policies_count = policies.count()
        accepted_policies_count = len(accepted_policies_ids)
        all_policies_accepted = accepted_policies_count == total_policies_count

        context = {
             self.context_object_name: policies,
            'accepted_policies_ids': accepted_policies_ids,
            'all_policies_accepted': all_policies_accepted,
        }
       
        return render(request, self.template_name, context)
        

    def post(self, request):
        
        policies = Policies.objects.all()
        accepted_policies = []

        for policy in policies:
            accepted = request.POST.get(f'policy_{policy.id}')
            if accepted == 'on':
                accepted_policies.append(UserAcceptedPolicies(user=request.user, policies=policy, accepted=True))

        UserAcceptedPolicies.objects.bulk_create(accepted_policies)
        
        # Retrieve the user's profile
        
        accepted_policies = UserAcceptedPolicies.objects.filter(user=request.user)
        accepted_policies_ids = [policy.policies_id for policy in accepted_policies]
        total_policies_count = policies.count()
        accepted_policies_count = len(accepted_policies_ids)
        all_policies_accepted = accepted_policies_count == total_policies_count
        
        if all_policies_accepted == True:
            # Retrieve the user's profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            #profile = Profile.objects.get(user=request.user)
            
            # Update the  companyPolices_completed field to True
            profile.companyPolices_completed = True
            profile.save()
            
        # Update is_accepted context states to True    
        request.session['is_accepted'] = True

        messages.success(request, 'Policies accepted successfully.')
        return redirect('employee:profile_building_progress')
        
class AcceptPoliciesView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        policies = UserAcceptedPolicies.objects.filter(user=user, accepted=False)

        if policies:
            for policy in policies:
                policy.accepted = True
                policy.save()

            # Update BasicInfo model
            user.profile.is_accepted = True
            user.profile.save()

            # Redirect to success page or home page
            return redirect('employee:policies_list')

        # Redirect to some error page if no policies found
        return redirect('employee:policies_list')

class PoliciesAcceptForm(forms.Form):
    # Define form fields if needed
    pass

class PoliciesAcceptView(LoginRequiredMixin, FormView):
    template_name = 'employee/policies_accept.html'
    form_class = PoliciesAcceptForm
    success_url = reverse_lazy('employee:policies_list')

    def form_valid(self, form):
        policy_slug = self.kwargs['slug']
        policy = Policies.objects.get(slug=policy_slug)
        user = self.request.user

        accepted_policy = UserAcceptedPolicies.objects.create(
            user=user,
            policies=policy,
            accepted=True
        )
        accepted_policy.save()

        return redirect(self.success_url)

class PoliciesListView(ListView):
    model = Policies
    template_name = 'employee/policies_list.html'

class PoliciesDetailView(DetailView):
    model = Policies
    template_name = 'employee/policies_detail.html'
    
class PoliciesAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='admin').exists()

class PoliciesCreateView(PoliciesAdminRequiredMixin, CreateView):
    model = Policies
    template_name = 'employee/policies_create.html'
    fields = ['title', 'description', 'slug']
    success_url = reverse_lazy('employee:policies_list')

class PoliciesUpdateView(PoliciesAdminRequiredMixin, UpdateView):
    model = Policies
    template_name = 'employee/policies_update.html'
    fields = ['title', 'description', 'slug']
    success_url = reverse_lazy('employee:policies_list')

class PoliciesDeleteView(PoliciesAdminRequiredMixin, DeleteView):
    model = Policies
    template_name = 'employee/policies_delete.html'
    success_url = reverse_lazy('employee:policies_list')

#-----BasicInformation-----------------------------
class BasicInformationListView(LoginRequiredMixin, ListView):
    model = BasicInformation
    template_name = 'employee/basic_information_list.html'
    context_object_name = 'basic_information'

class BasicInformationCreateView(LoginRequiredMixin, CreateView):
    model = BasicInformation
    form_class = BasicInformationForm
    template_name = 'employee/basic_information_create.html'
    success_url = reverse_lazy('employee:basic_information_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        #profile = Profile.objects.get(user=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        if not profile.companyPolices_completed:
            # Redirect to Basic Information step if it is not completed
            return redirect('employee:policies_list')
        # Update the  companyPolices_completed field to True
        profile.basic_information_completed = True
        profile.save()
        return super().dispatch(request, *args, **kwargs)
    
class BasicInformationDetailView(LoginRequiredMixin, DetailView):
    model = BasicInformation
    template_name = 'employee/basic_information_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
class BasicInformationUpdateView(LoginRequiredMixin, UpdateView):
    model = BasicInformation
    form_class = BasicInformationForm
    template_name = 'employee/basic_information_update.html'
    
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('employee:basic_information_list')
    
    def dispatch(self, request, *args, **kwargs):
        #profile = Profile.objects.get(user=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        if not profile.companyPolices_completed:
            # Redirect to Basic Information step if it is not completed
            return redirect('employee:policies_list')
        return super().dispatch(request, *args, **kwargs)

class BasicInformationDeleteView(LoginRequiredMixin, DeleteView):
    model = BasicInformation
    template_name = 'employee/basic_information_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('employee:basic_information_list')


#Personal 
class PersonalCreateView(LoginRequiredMixin, CreateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'employee/personal_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('employee:personal_list')

    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.basic_information_completed:
            return redirect('employee:basic_information_create')
        
        profile.personal_information_completed = True
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)

class PersonalUpdateView(LoginRequiredMixin, UpdateView):
    model = Personal
    form_class = PersonalForm
    template_name = 'employee/personal_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse('employee:personal_list')

    def dispatch(self, request, *args, **kwargs):
        #profile = Profile.objects.get(user=request.user)
        try:
            # Retrieve the user's profile
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # If the profile doesn't exist, create a new one
            profile = Profile(user=request.user)
            
        if not profile.basic_information_completed:
            # Redirect to Basic Information step if it is not completed
            return redirect('employee:basic_information_create')
        profile.personal_information_completed = True
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.social_security_number = mask_ssn(obj.social_security_number)  # Mask the social security number
        return obj
    
class PersonalDetailView(LoginRequiredMixin, DetailView):
    model = Personal
    template_name = 'employee/personal_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'employee.can_view_sensitive_data'  # Custom permission required to view sensitive data

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personal_instance = self.get_object()
        social_security_number = personal_instance.social_security_number
        masked_ssn = mask_ssn(social_security_number)  # Apply custom template filter
        context['masked_ssn'] = masked_ssn
        return context
    
    
    def get_queryset(self):
        # Only allow the user who owns the profile to view it
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
class PersonalListView(LoginRequiredMixin, ListView):
    model = Personal
    template_name = 'employee/personal_list.html'
    context_object_name = 'personal_list'
    paginate_by = 10

    def get_queryset(self):
        return Personal.objects.filter(user=self.request.user)

class PersonalDeleteView(LoginRequiredMixin, DeleteView):
    model = Personal
    template_name = 'employee/personal_confirm_delete.html'
    success_url = reverse_lazy('employee:personal_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

#Military
class MilitaryCreateView(LoginRequiredMixin, CreateView):
    model = Military
    form_class = MilitaryForm
    template_name = 'employee/military_create.html'
    success_url = reverse_lazy('employee:military_create')
    
    def form_valid(self, form):
        # Set the user field to the currently logged-in user
        form.instance.user = self.request.user

        # Check if a Military record already exists for the user
        military_qs = Military.objects.filter(user=self.request.user)
        if military_qs.exists():
            # Update the existing Military record with the form data
            military = military_qs.first()
            military.branch = form.cleaned_data['branch']
            military.rank = form.cleaned_data['rank']
            military.discharge_year = form.cleaned_data['discharge_year']
            military.duty_flag = form.cleaned_data['duty_flag']
            military.certification_license = form.cleaned_data['certification_license']
            military.save()
        else:
            # Create a new Military record for the user
            military = form.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('employee:military_list')

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        profile.Military_completed = True
        profile.save()
        return super().dispatch(request, *args, **kwargs)
    
class MilitaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Military
    form_class = MilitaryForm
    template_name = 'employee/military_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('employee:military_list')

class MilitaryDetailView(LoginRequiredMixin, DetailView):
    model = Military
    template_name = 'employee/military_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class MilitaryListView(LoginRequiredMixin, ListView):
    model = Military
    template_name = 'employee/military_list.html'
    context_object_name = 'military_list'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class MilitaryDeleteView(LoginRequiredMixin, DeleteView):
    model = Military
    template_name = 'employee/military_confirm_delete.html'
    success_url = reverse_lazy('employee:military_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


#Education
class EducationListView(LoginRequiredMixin, ListView):
    model = Education
    template_name = 'employee/education_list.html'
    context_object_name = 'education_list'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        certification_licenses = CertificationLicense.objects.filter(education__user=self.request.user)
        context['certification_licenses'] = certification_licenses
        return context

class EducationDetailView(LoginRequiredMixin, DetailView):
    model = Education
    template_name = 'employee/education_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'employee/education_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('employee:education_list')

    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        if not profile.Military_completed:
            return redirect('employee:military_list')

        profile.Education_completed = True
        profile.save()

        return super().dispatch(request, *args, **kwargs)
       
class EducationUpdateView(LoginRequiredMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'employee/education_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('employee:education_list')
    
class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education
    template_name = 'employee/education_confirm_delete.html'
    success_url = reverse_lazy('employee:education_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
#CertificationLicense    
class CertificationLicenseListView(LoginRequiredMixin, ListView):
    model = CertificationLicense
    template_name = 'employee/certification_license_list.html'
    context_object_name = 'certification_license_list'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(education__user=self.request.user)

class CertificationLicenseCreateView(LoginRequiredMixin, CreateView):
    model = CertificationLicense
    form_class = CertificationLicenseForm
    template_name = 'employee/certification_license_create.html'
    success_url = reverse_lazy('employee:certification_license_list')

    def form_valid(self, form):
        education = Education.objects.filter(user=self.request.user).first()
        form.instance.education = education
        return super().form_valid(form)

class CertificationLicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = CertificationLicense
    template_name = 'employee/certification_license_update.html'
    fields = ['education', 'document_name', 'certification_file']
    success_url = reverse_lazy('employee:certification_license_list')

class CertificationLicenseDeleteView(LoginRequiredMixin, DeleteView):
    model = CertificationLicense
    template_name = 'employee/certification_license_delete.html'
    success_url = reverse_lazy('employee:certification_license_list')

class CertificationLicenseDetailView(LoginRequiredMixin, DetailView):
    model = CertificationLicense
    template_name = 'employee/certification_license_detail.html'
    context_object_name = 'certification_license'
    

#Experience
class ExperienceListView(LoginRequiredMixin, ListView):
    model = Experience
    template_name = 'employee/experience_list.html'
    context_object_name = 'experienceList'
    paginate_by = 10

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)
    
class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Military
    form_class = MilitaryForm
    template_name = 'employee/military_create.html'
    success_url = reverse_lazy('employee:military_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('employee:experience_list')

    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.Education_completed:
            return redirect('employee:education_list')
        
        profile.Experience_completed = True
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)
    
class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'employee/experience_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('employee:experience_list')
    
class ExperienceDetailView(LoginRequiredMixin, DetailView):
    model = Experience
    template_name = 'employee/experience_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
class ExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'employee/experience_confirm_delete.html'
    success_url = reverse_lazy('employee:experience_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
# No ExperienceView   
class NoExperienceView(LoginRequiredMixin, View):
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.Experience_completed = True
        profile.save()
        messages.success(request, 'No ExperienceView saved successfully.')
        return redirect('employee:profile_building_progress')

#EmployeePreferences
class EmployeePreferencesListView(LoginRequiredMixin,ListView):
    model = EmployeePreferences
    template_name = 'employee/preferences/employeePreferences_list.html'
    context_object_name = 'preferences_list'
    paginate_by = 10

    def get_queryset(self):
        return EmployeePreferences.objects.filter(user=self.request.user)
    
   
class EmployeePreferencesCreateView(LoginRequiredMixin, CreateView):
    model = EmployeePreferences
    form_class = EmployeePreferencesForm
    template_name = 'employee/preferences/employeePreferences_create.html'
    success_url = reverse_lazy('employee:employee-preferences-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.category_id = form.cleaned_data['category'].id  # Assign the category ID
        
        # Save the instance to the database
        self.object = form.save()
        
        # Get the selected positions and skills from the form data
        desired_positions = self.request.POST.getlist('desired_positions')
        skills = self.request.POST.getlist('skills')

        # Set the many-to-many relationships
        self.object.desired_positions.set(desired_positions)
        self.object.skills.set(skills)

        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        if not profile.Experience_completed:
            return redirect('employee:experience_list')

        profile.Preferences_completed = True
        profile.save()
        return super().dispatch(request, *args, **kwargs)



class EmployeePreferencesUpdateView(LoginRequiredMixin, UpdateView):
    model = EmployeePreferences
    form_class = EmployeePreferencesForm
    template_name = 'employee/preferences/employeePreferences_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return EmployeePreferences.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if 'preferences' in request.POST:
            employee_preferences_form = EmployeePreferencesForm(request.POST, instance=self.get_object())
            if employee_preferences_form.is_valid():
                employee_preferences = employee_preferences_form.save(commit=False)
                employee_preferences.category_id = request.POST.get('category')  # Set the category ID from the form data
                employee_preferences.user = request.user
                employee_preferences.save()  # Save the EmployeePreferences instance
                
                # Get the selected positions and skills from the form data
                desired_positions = request.POST.getlist('desired_positions')
                skills = request.POST.getlist('skills')

                # Clear existing desired_positions and skills and set the new values
                employee_preferences.desired_positions.clear()
                employee_preferences.skills.clear()
                employee_preferences.desired_positions.set(desired_positions)
                employee_preferences.skills.set(skills)
                
                return redirect('employee:employee-preferences-list')

        return super().post(request, *args, **kwargs)

class EmployeePreferencesDetailView(LoginRequiredMixin, DetailView):
    model = EmployeePreferences
    template_name = 'employee/preferences/employeePreferences_detail.html'
    context_object_name='preferences'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return EmployeePreferences.objects.filter(user=self.request.user)

class EmployeePreferencesDeleteView(LoginRequiredMixin, DeleteView):
    model = EmployeePreferences
    template_name = 'employee/preferences/employeePreferences_confirm_delete.html'
    success_url = reverse_lazy('employee:employee-preferences-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return EmployeePreferences.objects.filter(user=self.request.user)

