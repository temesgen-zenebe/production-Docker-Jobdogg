from django.views.generic import ListView, DetailView, FormView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Policies, Profile, UserAcceptedPolicies,BasicInformation
from django.contrib import messages
from django.template import Library
from django import forms
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .models import Personal, Language
from .forms import PersonalForm,BasicInformationForm
from employee.templatetags.mask_ssn import mask_ssn


#----Policies Models ------
class DashboardInformation(LoginRequiredMixin, View):
    template_name = 'employee/dashboardInfo.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    
#----Policies Models ------
class ProfileBuildingProgress(LoginRequiredMixin, View):
    template_name = 'employee/profileBuildingProgress.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)   
    
         
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
        return redirect('employee:policies_list')
        
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

# ----end-------

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


# Personal Create View
class PersonalCreateView(LoginRequiredMixin, CreateView):
    model = Personal
    form_class = PersonalForm 
    template_name = 'employee/personal_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('employee:personal_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

# Personal Update View
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
    
# Personal Detail View
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
    
# Personal List View
class PersonalListView(LoginRequiredMixin, ListView):
    model = Personal
    template_name = 'employee/personal_list.html'
    context_object_name = 'personal_list'
    paginate_by = 10

    def get_queryset(self):
        return Personal.objects.filter(user=self.request.user)


# Personal Delete View
class PersonalDeleteView(LoginRequiredMixin, DeleteView):
    model = Personal
    template_name = 'employee/personal_confirm_delete.html'
    success_url = reverse_lazy('employee:personal_list')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


