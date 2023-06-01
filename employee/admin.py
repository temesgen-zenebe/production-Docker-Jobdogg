from django.contrib import admin
from .models import (
     Profile, Policies, UserAcceptedPolicies,BasicInformation,Personal,Language
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