from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from employee.templatetags.mask_ssn import mask_ssn
from django.views import View
import logging

from employer.models import SocCode
logger = logging.getLogger(__name__)

from django.views.generic import (ListView, CreateView, UpdateView, DetailView, DeleteView, FormView)

from .models import (
    BankAccount, Card, Category,CertificationLicense, CheckByEmail, EWallet,Education,EmployeePreferences,Experience, 
    Policies,Position,Profile, RidePreference, Skill, SkillSetTestResult, TaxDocumentSetting,UserAcceptedPolicies,
    BasicInformation,Personal,Military,Safety_Video_and_Test, VideoResume, 
    Background_Check,    
)

from .forms import (
    BackgroundCheckFormUpdate,
    BankAccountForm,
    BasicInformationForm,
    CertificationLicenseForm,
    CheckByEmailForm,
    EWalletForm,
    EducationForm,
    EmployeePreferencesForm,
    ExperienceForm,
    MilitaryForm,
    PersonalForm,
    ExperienceForm,
    MilitaryForm,
    PersonalForm,
    BasicInformationForm,
    SafetyTestResultForm,
    TaxDocumentSettingForm,
    VideoResumeForm,
    BackgroundCheckForm,
    CardForm,  
    RidePreferenceForm, 
)

#---- Models ------
class DashboardInformation(LoginRequiredMixin, View):
    template_name = 'employee/dashboardInfo.html'

    def get(self, request):
        # Get the user's profile
        profiles = Profile.objects.filter(user=request.user).first()
        
        context = {
            'paymentPref': profiles,
        }
        return render(request, self.template_name, context)
    
#----Profile Models ------
class ProfileBuildingProgress(LoginRequiredMixin, View):
    template_name = 'employee/profileBuildingProgress.html'
    
    def get_progress_percentage(self, profile):
        total_steps = 14  # Total number of steps in the profile
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
                profile.Safety_Video_and_Test_completed,
                profile.VideoResume_completed,
                profile.Background_Check_completed,
                profile.Treat_Box_completed,
                profile.Select_Ride_completed,
            ]
        )
        progress_percentage = (completed_steps / total_steps) * 100
        return int(progress_percentage)
    
    def get(self, request):
        
        #progress_percentage = 50.0  # Replace this with the actual progress_percentage value you want to display
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
        safetyVideo_form = SafetyTestResultForm()
        videoResume_form = VideoResumeForm()
        BackgroundCheck_form= BackgroundCheckForm()
        BankAccount_form = BankAccountForm()
        Card_form =CardForm()
        EWallet_form= EWalletForm()
        CheckByEmail_form=CheckByEmailForm()
        RidePreference_form = RidePreferenceForm()
        progress = Profile.objects.filter(user=request.user)
        profile = get_object_or_404(Profile, user=request.user)
        profiles = Profile.objects.filter(user=request.user).first()
        progress_percentage = self.get_progress_percentage(profile)
        categories = Category.objects.all()
        positions = Position.objects.all()
        skills = Skill.objects.all()
        safetyVideo = Safety_Video_and_Test.objects.all()
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
            'safetyVideo_form':safetyVideo_form,
            'progress':progress,
            'paymentPref': profiles,
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
            'safetyVideo':safetyVideo,
            'videoResume_form' :videoResume_form,
            'BackgroundCheck_form':BackgroundCheck_form,
            'BankAccount_form':BankAccount_form,
            'Card_form':Card_form,
            'EWallet_form':EWallet_form,
            'CheckByEmail_form':CheckByEmail_form,
            'RidePreference_form':RidePreference_form,
            
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
                    
        elif 'safetyVideoTesting' in request.POST:
            SafetyTestResult_form = SafetyTestResultForm(request.POST)
            if SafetyTestResult_form.is_valid():
               SafetyTestResult = SafetyTestResult_form.save(commit=False)
               SafetyTestResult.user = request.user
               SafetyTestResult.save()
               # Update the profile building process states
               
               profile.Safety_Video_and_Test_completed = True
               profile.save()
               
               return redirect('employee:profile_building_progress')
            else:
              print("Safety Test Result form is invalid")
              
        elif 'uploadVideoResumeFormSubmit' in request.POST:
            VideoResumeSubmited_form = VideoResumeForm(request.POST, request.FILES)
            if VideoResumeSubmited_form.is_valid():
                VideoResume = VideoResumeSubmited_form.save(commit=False)
                VideoResume.user = request.user
                VideoResume.save()
                # Update the profile building process states
                profile.VideoResume_completed = True
                profile.save()
                return redirect('employee:profile_building_progress')
            else:
                print("VideoResume form is invalid")
                
        elif 'addToBackgroundCheckProfile' in request.POST:
            background_check_form = BackgroundCheckForm(request.POST, request.FILES)
            if background_check_form.is_valid():
                background_check = background_check_form.save(commit=False)
                background_check.user = request.user
                background_check.save()
                # Update the profile building process states
                profile.Background_Check_completed = True
                profile.save()
                return redirect('employee:profile_building_progress')
            else:
                print("BackgroundCheckProfile form is invalid") 
                
        elif 'BankAccountOptionSubmission' in request.POST:
            bankAccount_form = BankAccountForm(request.POST)
            if bankAccount_form.is_valid():
                bankAccount = bankAccount_form.save(commit=False)
                bankAccount.user = request.user
                bankAccount.save()
                # Update the profile building process states
                profile.Treat_Box_completed = True
                profile.bankAccountBtn_completed = True
                profile.CheckByMailBtn_completed=False
                profile.eWalletBtn_completed=False
                profile.cardBtn_completed=False
                
                profile.save()
                return redirect('employee:profile_building_progress')
            else:
                print("bankAccount form is invalid") 
            
        elif 'cardOptionSubmission' in request.POST:
            cardForm_form = CardForm(request.POST)
            if cardForm_form.is_valid():
               cardForm = cardForm_form.save(commit=False)
               cardForm.user = request.user
               cardForm.save()
               # Update the profile building process states
               profile.Treat_Box_completed = True
               profile.cardBtn_completed=True
               profile.CheckByMailBtn_completed=False
               profile.eWalletBtn_completed=False
               profile.bankAccountBtn_completed=False
               profile.save()
               return redirect('employee:profile_building_progress')
            else:
               print("Card form is invalid:", cardForm_form.errors) 
               
        
        elif 'eWalletFormSubmission' in request.POST:
            eWallet_form = EWalletForm(request.POST)
            if eWallet_form.is_valid():
               eWallet = eWallet_form.save(commit=False)
               eWallet.user = request.user
               eWallet.save()
               # Update the profile building process states
               profile.Treat_Box_completed = True
               profile.eWalletBtn_completed =True
               profile.CheckByMailBtn_completed=False
               profile.cardBtn_completed=False
               profile.bankAccountBtn_completed=False
               profile.save()
               return redirect('employee:profile_building_progress')
            else:
               print("Card form is invalid:", eWallet_form.errors)
        
        elif 'CheckByEmailFormSubmission' in request.POST:
            checkByEmail_form = CheckByEmailForm(request.POST)
            if checkByEmail_form.is_valid():
               checkByEmail = checkByEmail_form.save(commit=False)
               checkByEmail.user = request.user
               checkByEmail.save()
               # Update the profile building process states
               profile.Treat_Box_completed=True
               profile.CheckByMailBtn_completed=True
               profile.eWalletBtn_completed=False
               profile.cardBtn_completed=False
               profile.bankAccountBtn_completed=False
               profile.save()
               return redirect('employee:profile_building_progress')
            else:
               print("Card form is invalid:", checkByEmail_form.errors)
               
        elif 'ridePreferenceFormSubmit' in request.POST:
            ridePreference_form = RidePreferenceForm(request.POST)
            if ridePreference_form.is_valid():
                RidePreference = ridePreference_form.save(commit=False)
                RidePreference.user = request.user
                RidePreference.save()
                # Update the profile building process states
                profile.Select_Ride_completed = True
                profile.save()
                return redirect('employee:profile_building_progress')
            else:
                print("VideoResume form is invalid")       
            
               
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
        safetyVideo_form = SafetyTestResultForm()
        videoResume_form = VideoResumeForm()
        BackgroundCheck_form= BackgroundCheckForm()
        BankAccount_form = BankAccountForm()
        Card_form =CardForm()
        EWallet_form= EWalletForm()
        CheckByEmail_form=CheckByEmailForm()
        RidePreference_form = RidePreferenceForm()
        context = {
            'basic_information_form': basic_information_form,
            'personal_form': personal_form,
            'military_form':military_form,
            'education_form':education_form,
            'CertificationLicense_form':CertificationLicense_form,
            'experienceForm_form':experienceForm_form,
            'employee_preferences_form': employee_preferences_form,
            'safetyVideo_form':safetyVideo_form,
            'videoResume_form':videoResume_form,
            'BackgroundCheck_form':BackgroundCheck_form,
            'BankAccount_form':BankAccount_form,
            'Card_form':Card_form,
            'EWallet_form':EWallet_form,
            'CheckByEmail_form':CheckByEmail_form,
            'RidePreference_form':RidePreference_form,
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
        OnSkipSkill = get_object_or_404(SkillSetTestResult, user=request.user).first()
        profile.OnProgressSkillTest_completed = True
        profile.Skipped_completed = False
        profile.SkillSetTest_completed = False
        OnSkipSkill.states = 'in-progress'
        profile.save()
        OnSkipSkill.save()
        messages.success(request, 'Skip SkillSet OnPrecess successfully.')
        return redirect('employee:profile_building_progress')  

#generating 
class GenerateSkillTestView(View):
    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        user_preferences = get_object_or_404(EmployeePreferences, user=request.user)
        positions = user_preferences.desired_positions.all()

        # Assuming you want to get the first position from the list of desired positions
        assigned_position = positions.first()  # Update this logic if needed

        assigned_test = get_object_or_404(Position, position=assigned_position.position)  # Retrieve the Position instance
        test_link = assigned_test.skill_test_link

        # Create the SkillSetTestResult object
        SkillSetTestResult.objects.create(
            user=request.user,
            position=assigned_test,  # Assign the Position instance, not the position name
            skill_test=test_link,
            states = 'in-progress'
        )
        
        profile.OnProgressSkillTest_completed = True
        profile.Skipped_completed = False
        profile.SkillSetTest_completed = False
        profile.save()
        messages.success(request, 'SkillSet created successfully.')
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
    
    def get_queryset(self):
        return BasicInformation.objects.filter(user=self.request.user)

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
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
class BasicInformationUpdateView(LoginRequiredMixin, UpdateView):
    model = BasicInformation
    form_class = BasicInformationForm
    template_name = 'employee/basic_information_update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    
    def get_success_url(self):
        return reverse_lazy('employee:basic_information_list')
    
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
    model = Experience
    form_class = ExperienceForm
    template_name = 'employee/experience_create.html'
    success_url = reverse_lazy('employee:experience_list')

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


#SkillSetTestResultList
class SkillSetTestResultListView(LoginRequiredMixin,ListView):
    model = SkillSetTestResult
    template_name = 'employee/skillsettestresult/skillsettestresult_list.html'
    context_object_name = 'skillsettestresults'
    paginate_by = 10

    def get_queryset(self):
        return SkillSetTestResult.objects.filter(user=self.request.user)

class SkillSetTestResultCreateView(LoginRequiredMixin,CreateView):
    model = SkillSetTestResult
    template_name = 'employee/skillsettestresult/skillsettestresult_form.html'
    fields = ['user', 'position', 'skill_test', 'states', 'result']
    success_url = reverse_lazy('employee:skillsettestresult-list')

class SkillSetTestResultUpdateView(LoginRequiredMixin,UpdateView):
    model = SkillSetTestResult
    template_name = 'employee/skillsettestresult/skillsettestresult_form.html'
    fields = ['result','conformation']
    success_url = reverse_lazy('employee:skillsettestresult-list')
    
    def get_queryset(self):
        return SkillSetTestResult.objects.filter(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
            completedSkill = SkillSetTestResult.objects.filter(user=request.user).order_by('-created').first()
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            completedSkill = SkillSetTestResult(user=request.user)
        if not profile.Preferences_completed:
            return redirect('employee:employee-preferences-create')

        profile.SkillSetTest_completed = True
        profile.OnProgressSkillTest_completed = False
        profile.Skipped_completed = False
        completedSkill.states = 'pending'
        profile.save()
        completedSkill.save()
        return super().dispatch(request, *args, **kwargs)

class SkillSetTestResultDeleteView(LoginRequiredMixin,DeleteView):
    model = SkillSetTestResult
    template_name = 'employee/skillsettestresult/skillsettestresult_confirm_delete.html'
    success_url = reverse_lazy('employee:skillsettestresult-list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return SkillSetTestResult.objects.filter(user=self.request.user)
      
class SkillSetTestResultDetailView(LoginRequiredMixin, DetailView):
    model = SkillSetTestResult
    template_name = 'employee/skillsettestresult/skillsettestresult_detail.html'
    context_object_name='skillSetTestResultList'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return SkillSetTestResult.objects.filter(user=self.request.user)
    
#SafetyVideoTest 
class SafetyVideoTestListView(LoginRequiredMixin, ListView):
    model = Safety_Video_and_Test
    template_name = 'employee/safetyVideoTest/safetyVideoTest_list.html'
    context_object_name = 'safetyVideoTest'
    
class SafetyVideoTestDetailView(LoginRequiredMixin, DetailView):
    model = Safety_Video_and_Test
    template_name = 'employee/safetyVideoTest/safetyVideoTest_detail.html'
    context_object_name = 'safetyVideoTestDetailView'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get a list of data entries for the given model
        context['related_entries'] = Safety_Video_and_Test.objects.all().order_by('-created_at')[:5]
        # increment view_count field by 1 every time the DetailView is accessed
        self.object.view_count += 1
        self.object.save()
        return context
    
class SafetyVideoTestCreateView(LoginRequiredMixin, CreateView):
    model = Safety_Video_and_Test
    template_name = 'employee/safetyVideoTest/safetyVideoTest_form.html'
    fields = ['title', 'image', 'video_url', 'description']
    success_url = reverse_lazy('employee:safetyVideoTest_list')
    extra_context = {'is_create': True}
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SafetyVideoTestUpdateView(LoginRequiredMixin, UpdateView):
    model = Safety_Video_and_Test
    template_name = 'employee/safetyVideoTest/safetyVideoTest_form.html'
    fields = ['title', 'image', 'video_url', 'description']
    success_url = reverse_lazy('employee:safetyVideoTest_list')
    extra_context = {'is_create': False}

class SafetyVideoTestDeleteView(LoginRequiredMixin, DeleteView):
    model = Safety_Video_and_Test
    template_name = 'employee/safetyVideoTest/safetyVideoTest_confirm_delete.html'
    success_url = reverse_lazy('employee:safetyVideoTest_list')



#videoResume
class VideoResumeListView(LoginRequiredMixin, ListView):
    model = VideoResume
    template_name = 'employee/videoResume/video_resume_list.html'
    context_object_name = 'video_resumes'
    
class VideoResumeDetailView(LoginRequiredMixin, DetailView):
    model = VideoResume
    template_name = 'employee/videoResume/video_resume_detail.html'
    context_object_name = 'video_resume_detail'

class VideoResumeCreateView(LoginRequiredMixin,CreateView):
    model = VideoResume
    form_class = VideoResumeForm
    template_name = 'employee/videoResume/video_resume_create.html'
    success_url = reverse_lazy('employee:video_resume_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.Safety_Video_and_Test_completed:
            return redirect('employee:safetyVideoTest_list')
        
        profile.VideoResume_completed = True
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)

class VideoResumeUpdateView(LoginRequiredMixin, UpdateView):
    model = VideoResume
    form_class = VideoResumeForm
    template_name = 'employee/videoResume/video_resume_update.html'
    success_url = reverse_lazy('employee:video_resume_list')
   
class VideoResumeDeleteView(LoginRequiredMixin, DeleteView):
    model = VideoResume
    template_name = 'employee/videoResume/video_resume_delete.html'
    success_url = reverse_lazy('employee:video_resume_list')
    
#backgroundCheck
class BackgroundCheckListView(LoginRequiredMixin,ListView):
    model = Background_Check
    template_name = 'employee/backgroundCheck/background_check_list.html'
    context_object_name = 'backgroundChecked'
    
class BackgroundCheckCreateView(LoginRequiredMixin, CreateView):
    model = Background_Check
    form_class = BackgroundCheckForm
    template_name = 'employee/backgroundCheck/background_check_create.html'
    success_url = reverse_lazy('employee:background_check_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()

        if not profile.VideoResume_completed:
            #print("Redirecting to BackgroundCheckCreateView.")
            return redirect('employee:video_resume_list')
        
        profile.Background_Check_completed = True
        profile.save()
            
        return super().dispatch(request, *args, **kwargs)
       
class BackgroundCheckDetailView(LoginRequiredMixin, DetailView):
    model = Background_Check
    template_name = 'employee/backgroundCheck/background_check_detail.html'
   
class BackgroundCheckUpdateView(LoginRequiredMixin, UpdateView):
    model = Background_Check
    form_class = BackgroundCheckFormUpdate
    template_name = 'employee/backgroundCheck/background_check_update.html'
    success_url = reverse_lazy('employee:background_check_list')
    
class BackgroundCheckDeleteView(LoginRequiredMixin, DeleteView):
    model = Background_Check
    template_name = 'employee/backgroundCheck/background_check_confirm_delete.html'
    success_url = reverse_lazy('employee:background_check_list')


#CheckByEmail
class CheckByEmailListView(LoginRequiredMixin, ListView):
    model = CheckByEmail
    template_name = 'employee/PaymentPreferences/checkByEmail/check_by_email_list.html'
    context_object_name = 'checks'

class CheckByEmailDetailView(LoginRequiredMixin, DetailView):
    model = CheckByEmail
    template_name = 'employee/PaymentPreferences/checkByEmail/check_by_email_detail.html'
    context_object_name = 'check'

class CheckByEmailCreateView(LoginRequiredMixin, CreateView):
    model = CheckByEmail
    template_name = 'employee/PaymentPreferences/checkByEmail/check_by_email_form.html'
    form_class = CheckByEmailForm
    success_url = reverse_lazy('employee:check_by_email_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.Background_Check_completed:
            return redirect('employee:background_check_list')
        
        profile.Treat_Box_completed = True
        profile.CheckByMailBtn_completed = True
        profile.eWalletBtn_completed=False
        profile.cardBtn_completed=False
        profile.bankAccountBtn_completed=False
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)

class CheckByEmailUpdateView(LoginRequiredMixin, UpdateView):
    model = CheckByEmail
    template_name = 'employee/PaymentPreferences/checkByEmail/check_by_email_update.html'
    form_class = CheckByEmailForm
    context_object_name = 'check'
    success_url = reverse_lazy('employee:check_by_email_list')
    
class CheckByEmailDeleteView(LoginRequiredMixin, DeleteView):
    model = CheckByEmail
    template_name = 'employee/PaymentPreferences/checkByEmail/check_by_email_confirm_delete.html'
    context_object_name = 'check'
    success_url = reverse_lazy('employee:check_by_email_list')

class EWalletListView(LoginRequiredMixin, ListView):
    model = EWallet
    template_name = 'employee/PaymentPreferences/eWallet/e_wallet_list.html'
    context_object_name = 'e_wallets'
    paginate_by = 10

class EWalletDetailView(LoginRequiredMixin, DetailView):
    model = EWallet
    template_name = 'employee/PaymentPreferences/eWallet/e_wallet_detail.html'
    context_object_name = 'e_wallet'

class EWalletCreateView(LoginRequiredMixin, CreateView):
    model = EWallet
    form_class = EWalletForm
    template_name = 'employee/PaymentPreferences/eWallet/e_wallet_create.html'
    success_url = reverse_lazy('employee:e_wallet_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.Background_Check_completed:
            return redirect('employee:background_check_list')
        
        profile.Treat_Box_completed = True
        profile.eWalletBtn_completed =True
        profile.CheckByMailBtn_completed=False
        profile.cardBtn_completed=False
        profile.bankAccountBtn_completed=False
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)

class EWalletUpdateView(LoginRequiredMixin, UpdateView):
    model = EWallet
    form_class = EWalletForm
    template_name = 'employee/PaymentPreferences/eWallet/e_wallet_update.html'
    context_object_name = 'e_wallet'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('employee:e_wallet_list')

class EWalletDeleteView(LoginRequiredMixin, DeleteView):
    model = EWallet
    template_name = 'employee/PaymentPreferences/eWallet/e_wallet_confirm_delete.html'
    context_object_name = 'e_wallet'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('employee:e_wallet_list')



#Card preference 
class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'employee/PaymentPreferences/Card/card_list.html'
    context_object_name = 'cards'
    paginate_by = 10

class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'employee/PaymentPreferences/Card/card_detail.html'
    context_object_name = 'card'

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    form_class = CardForm
    template_name = 'employee/PaymentPreferences/Card/card_create.html'
    success_url = reverse_lazy('employee:card_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.Background_Check_completed:
            return redirect('employee:background_check_list')
        
        profile.Treat_Box_completed = True
        profile.cardBtn_completed=True
        profile.CheckByMailBtn_completed=False
        profile.eWalletBtn_completed=False
        profile.bankAccountBtn_completed=False
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    form_class = CardForm
    template_name = 'employee/PaymentPreferences/Card/card_update.html'
    context_object_name = 'card'
    success_url = reverse_lazy('employee:card_list')

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    context_object_name = 'card'
    template_name = 'employee/PaymentPreferences/Card/card_confirm_delete.html'
    success_url = reverse_lazy('employee:card_list')

#BankAccountList
class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'employee/PaymentPreferences/bankAccount/bankAccount_list.html'
    context_object_name = 'bankAccounts'
    paginate_by = 10

class BankAccountDetailView(LoginRequiredMixin, DetailView):
    model = BankAccount
    template_name = 'employee/PaymentPreferences/bankAccount/bankAccount_detail.html'
    context_object_name = 'bankAccount'

class BankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = 'employee/PaymentPreferences/bankAccount/bankAccount_create.html'
    success_url = reverse_lazy('employee:bankAccount_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.Background_Check_completed:
            return redirect('employee:background_check_list')
        
        profile.Treat_Box_completed = True
        profile.bankAccountBtn_completed = True
        profile.CheckByMailBtn_completed=False
        profile.eWalletBtn_completed=False
        profile.cardBtn_completed=False
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)

class BankAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = 'employee/PaymentPreferences/bankAccount/bankAccount_update.html'
    context_object_name = 'bankAccount'
    success_url = reverse_lazy('employee:bankAccount_list')

class BankAccountDeleteView(LoginRequiredMixin, DeleteView):
    model = BankAccount
    template_name = 'employee/PaymentPreferences/bankAccount/bankAccount_confirm_delete.html'
    context_object_name = 'bankAccount'
    success_url = reverse_lazy('employee:bankAccount_list')
    
#RidePreference
class RidePreferenceListView(LoginRequiredMixin, ListView):
    model = RidePreference
    template_name = 'employee/ridePreference/ridePreference_list.html'
    context_object_name = 'ridePreference'
    paginate_by = 10

class RidePreferenceDetailView(LoginRequiredMixin, DetailView):
    model = RidePreference
    template_name = 'employee/ridePreference/ridePreference_detail.html'
    context_object_name = 'ridePreference'

class RidePreferenceCreateView(LoginRequiredMixin, CreateView):
    model = RidePreference
    form_class = RidePreferenceForm
    template_name = 'employee/ridePreference/ridePreference_create.html'
    success_url = reverse_lazy('employee:ridePreference_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            
        if not profile.Background_Check_completed:
            return redirect('employee:ridePreference_list')
        
        profile.Treat_Box_completed = True
        
        profile.save()
        
        return super().dispatch(request, *args, **kwargs)

class RidePreferenceUpdateView(LoginRequiredMixin, UpdateView):
    model = RidePreference
    form_class = RidePreferenceForm
    template_name = 'employee/ridePreference/ridePreference_update.html'
    context_object_name = 'ridePreference'
    success_url = reverse_lazy('employee:ridePreference_list')

class RidePreferenceDeleteView(LoginRequiredMixin, DeleteView): 
    model = RidePreference
    template_name = 'employee/ridePreference/ridePreference_confirm_delete.html'
    context_object_name = 'ridePreference'
    success_url = reverse_lazy('employee:ridePreference_list')
    
#TaxDocumentSetting  
class TaxDocumentSettingListView(LoginRequiredMixin, ListView):
    model = TaxDocumentSetting
    template_name = 'employee/TaxDocumentSetting/tax_document_setting_list.html'
    context_object_name = 'tax_document_settings'
    paginate_by = 10

class TaxDocumentSettingDetailView(LoginRequiredMixin, DetailView):
    model = TaxDocumentSetting
    template_name = 'employee/TaxDocumentSetting/tax_document_setting_detail.html'
    context_object_name = 'tax_document_setting'

class TaxDocumentSettingCreateView(LoginRequiredMixin, CreateView):
    model = TaxDocumentSetting
    form_class = TaxDocumentSettingForm
    template_name = 'employee/TaxDocumentSetting/tax_document_setting_form.html'
    success_url = reverse_lazy('employee:tax_document_setting_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaxDocumentSettingUpdateView(LoginRequiredMixin, UpdateView):
    model = TaxDocumentSetting
    form_class = TaxDocumentSettingForm
    template_name = 'employee/TaxDocumentSetting/tax_document_setting_update.html'
    context_object_name = 'tax_document_setting'
    success_url = reverse_lazy('employee:tax_document_setting_list')

class TaxDocumentSettingDeleteView(LoginRequiredMixin, DeleteView):
    model = TaxDocumentSetting
    template_name = 'employee/TaxDocumentSetting/tax_document_setting_confirm_delete.html'
    context_object_name = 'tax_document_setting'
    success_url = reverse_lazy('employee:tax_document_setting_list')