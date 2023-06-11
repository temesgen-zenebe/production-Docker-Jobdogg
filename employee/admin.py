from django.contrib import admin
from .models import (
     CertificationLicense, 
     Education,
     Experience, 
     Military, 
     Profile, 
     Policies,
     UserAcceptedPolicies,
     BasicInformation,
     Personal,
     Language
   
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display =[
                'user',
                'companyPolices_completed',
                'basic_information_completed', 
                'personal_information_completed',
                'Military_completed',
                'Education_completed',
                'Experience_completed', 
                'Preferences_completed', 
                'SkillSetTest_completed',
                'VideoResume_completed', 
                'ResumeUploading_completed'
            ]
    
@admin.register(Policies)
class PoliciesAdmin(admin.ModelAdmin):
    model = Policies
    list_display = ['title', 'description','created','updated','slug']
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created','updated','slug')
        return ()
    
@admin.register(UserAcceptedPolicies)
class UserAcceptedPoliciesAdmin(admin.ModelAdmin):
    model = UserAcceptedPolicies
    list_display = ['user', 'policies', 'accepted','created','updated','slug']
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('policies', 'accepted','created','updated','slug')
        return ()  

@admin.register(BasicInformation)
class BasicInformationAdmin(admin.ModelAdmin):
    model = BasicInformation
    list_display = [
    'user',
    'address',
    'apartment',
    'city',
    'state', 
    'zip_code',
    'cell_phone',
    'home_phone',
    'work_phone',
    'email',
    'emergency_contact_number', 
    'emergency_contact_name',
    'created', 
    'updated'
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
  
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    model = Language
    list_display = ['name']

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    model = Personal
    list_display = [
        'nickname', 
        'user', 
        'social_security_number',
        'drivers_license_state',
        'drivers_license_number',
        'date_of_birth', 
        'gender', 
        'e_verify',
        'slug',
        'created',
        'updated'
        ]
    list_filter = ('gender', 'e_verify')
    search_fields = ('nickname', 'user__username', 'user__email')
   
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
    
@admin.register(Military)
class MilitaryAdmin(admin.ModelAdmin):
    model = Military
    list_display = ['user', 'branch', 'rank', 'discharge_year', 'duty_flag','created','updated']
    list_filter = ('branch', 'rank', 'discharge_year', 'duty_flag')
   

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
    
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    model = Education
    list_display = ['user', 'school_name', 'degree_type', 'graduated','created','updated']
    list_filter = ('graduated',)
    search_fields = ('user__username', 'school_name', 'degree_type')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
    
@admin.register(CertificationLicense)
class CertificationLicenseAdmin(admin.ModelAdmin):
    model = CertificationLicense
    list_display = ['document_name', 'education', 'created', 'updated']
    prepopulated_fields = {'slug': ['document_name']}
  
    
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'job_title', 'start_date', 'end_date']
    search_fields = ('user__username', 'company_name', 'job_title')
    list_filter = ('start_date', 'end_date')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()