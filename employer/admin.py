from django.contrib import admin
from common.utils.text import unique_slug
from .models import CompanyProfile, EmployerAcceptedPolicies, EmployerPoliciesAndTerms, HiredEmployeeList, JobRequisition, ProfileBuildingController, SocCode

from django.contrib import admin
from .models import ProfileBuildingController

@admin.register(ProfileBuildingController)
class ProfileBuildingControllerAdmin(admin.ModelAdmin):
    list_display = ('user', 
                    'is_account_created', 'is_company_profile_created', 
                    'is_payment_information_created', 'is_police_accepted_created', 
                    'is_contract_signed_created', 'is_payment_plan_validated',
                    'is_billing_information_created', 'created', 'updated')
    
    list_filter = ('is_account_created', 'is_company_profile_created',
                   'is_payment_information_created', 'is_police_accepted_created',
                   'is_contract_signed_created', 'is_payment_plan_validated',
                   'is_billing_information_created', 'created', 'updated')
    
    search_fields = ('user__username',)
    

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = unique_slug(f"{obj.user.username}", ProfileBuildingController)
        super().save_model(request, obj, form, change)



@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'representative_full_name', 'industry', 'created', 'updated')
    list_filter = ('industry', 'created', 'updated')
    search_fields = ('company_name', 'representative_full_name', 'email')

    fieldsets = (
        ('Basic Information', {
            'fields': ('user','company_name', 'logo', 'headquarters_address', 'city', 'state', 'country', 'zip_code')
        }),
        ('Contact Information', {
            'fields': ('telephone', 'email', 'fax', 'website')
        }),
        ('Representative Information', {
            'fields': ('representative_full_name', 'Department')
        }),
        ('Additional Information', {
            'fields': ('employees', 'industry', 'description', 'video', 'opening_hours', 'google_map_link')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = unique_slug(f"{obj.company_name} {obj.user.username}", CompanyProfile)
        super().save_model(request, obj, form, change)


@admin.register(EmployerPoliciesAndTerms)
class EmployerPoliciesAndTermsAdmin(admin.ModelAdmin):
    model = EmployerPoliciesAndTerms
    list_display = ['title','created','updated','slug']
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created','updated','slug')
        return ()
    
@admin.register(EmployerAcceptedPolicies)
class EmployerAcceptedPoliciesAdmin(admin.ModelAdmin):
    model = EmployerAcceptedPolicies
    list_display = ['user', 'policies', 'accepted','created','updated','slug']
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('policies', 'accepted','created','updated','slug')
        return ()  
    
@admin.register(SocCode)
class SocCodeAdmin(admin.ModelAdmin):
    model=SocCode
    list_display = ('soc_code',)   


@admin.register(JobRequisition)
class JobRequisitionAdmin(admin.ModelAdmin):
    model=JobRequisition
    list_display = (
        'user', 'industry', 'get_job_titles', 'get_required_skills',
        'min_salary_amount', 'job_type', 'soc_code','city', 'state', 
        'zip_code','preference_action','created', 'updated', 'slug'
    )
    list_filter = ('industry','job_type', 'city', 'state', 'created', 'updated')
    search_fields = ('user__username', 'industry__name', 'job_type',  'department', 'city', 'state', 'zip_code')

    def get_job_titles(self, obj):
        return ", ".join([str(position) for position in obj.job_title.all()])

    get_job_titles.short_description = 'Job Titles'

    def get_required_skills(self, obj):
        return ", ".join([str(skill) for skill in obj.required_skills.all()])

    get_required_skills.short_description = 'required skills'

    
@admin.register(HiredEmployeeList)
class HiredEmployeeListAdmin(admin.ModelAdmin):
    model = HiredEmployeeList
    list_display = ('user', 'employee_name', 'employee_ID', 'hired_date', 'created', 'updated')
    search_fields = ['user__username', 'employee_name', 'employee_ID']
    list_filter = ['hired_date']


    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created','updated','slug')
        return ()    