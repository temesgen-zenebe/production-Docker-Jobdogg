from django.contrib import admin

from common.utils.text import unique_slug
from .models import (
    BankAccount, Education, Background_Check,CertificationLicense,CheckByEmail,EWallet, 
    Experience, Military, Profile, Policies, RidePreference,SafetyTestResult, TaxDocumentSetting,UserAcceptedPolicies,
    BasicInformation, SkillSetTestResult,Safety_Video_and_Test,VideoResume,
    RettingCommenting,Card,
     
     #Personal
     Personal,
     Language,
     
     #preferences
     Category, 
     Position, 
     Skill, 
     EmployeePreferences, 
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display =[
                'user',
                'account_created',
                'companyPolices_completed',
                'basic_information_completed', 
                'personal_information_completed',
                'Military_completed',
                'Education_completed',
                'Experience_completed', 
                'Preferences_completed', 
                'Skipped_completed' ,
                'OnProgressSkillTest_completed' ,
                'SkillSetTest_completed',
                'Safety_Video_and_Test_completed',
                'VideoResume_completed', 
                'Background_Check_completed',
                'Treat_Box_completed',
                'Select_Ride_completed',
                'cardBtn_completed',
                'eWalletBtn_completed',              
                'bankAccountBtn_completed',
                'CheckByMailBtn_completed',  
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
    list_display = ['user', 'company_name', 'company_phone','job_title', 'start_date', 'end_date','is_current','description']
    search_fields = ('user__username', 'company_name', 'job_title')
    list_filter = ('start_date', 'end_date')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('position', 'category', 'skill_test_link')
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill',)
    
@admin.register(EmployeePreferences)
class EmployeePreferencesAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'category', 'minimum_salary', 'job_type', 'location', 'work_arrangement_preference', 'can_relocation', 'years_of_experience', 'created', 'updated')
    list_filter = ('job_type', 'location', 'work_arrangement_preference', 'can_relocation', 'years_of_experience', 'created', 'updated')
    search_fields = ('user__username', 'category__name', 'desired_positions__name', 'skills__name')
   
    def get_desired_positions(self, obj):
        return ", ".join([str(position) for position in obj.desired_positions.all()])

    get_desired_positions.short_description = 'Desired Positions'

    def get_skills(self, obj):
        return ", ".join([str(skill) for skill in obj.skills.all()])

    get_skills.short_description = 'Skills'

#SkillSetTestResult
@admin.register(SkillSetTestResult)
class SkillSetTestResultAdmin(admin.ModelAdmin):
    model = SkillSetTestResult
    list_display = ['user','position', 'skill_test','states','result','conformation','slug', 'created','updated']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()


@admin.register(Safety_Video_and_Test)
class Safety_Video_and_TestAdmin(admin.ModelAdmin):
    model = Safety_Video_and_Test
    list_display = [
        'title',
        'image', 
        'video_url', 
        'description',
        'created_at', 
        'updated_at', 
        'view_count',
    ]
   

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created_at', 'updated_at')
        return ()
   
#SafetyTestResult 
@admin.register(SafetyTestResult)
class SafetyTestResultAdmin(admin.ModelAdmin):
    model = SafetyTestResult
    list_display =['user', 'safety_result','states','slug','created','updated']
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created', 'updated','slug')
        return ()
    
 #VideoResume 

@admin.register(VideoResume)
class VideoResumeAdmin(admin.ModelAdmin):
    model = VideoResume
    list_display =['user', 'video', 'tell_about_you','states','viewCount','slug','created','updated']
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created', 'updated','slug')
        return ()   

 #RettingCommenting

@admin.register(RettingCommenting)
class RettingCommentingAdmin(admin.ModelAdmin):
    model = RettingCommenting
    list_display =['user', 'retting', 'tag','comments','slug','created','updated']
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created', 'updated','slug')
        return ()
    


 #Background_Check

@admin.register(Background_Check)
class Background_CheckAdmin(admin.ModelAdmin):
    model = Background_Check
     
    list_display =[
        'user', 
        'certification_file', 
        'expiration_date',
        'expiration_states',
        'states',
        'slug',
        'created',
        'updated'
        ]
   
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created', 'updated','slug')
        return ()
    
@admin.register(CheckByEmail)
class CheckByEmailAdmin(admin.ModelAdmin):
    model = CheckByEmail
    list_display = ['user', 'method_type', 'poBox', 'use_basicInfo_address', 'valid', 'slug', 'created', 'updated']
    list_filter = ('user', 'method_type', 'valid', 'created', 'updated')
    search_fields = ('user__username', 'method_type', 'poBox')
    readonly_fields = ('slug','created', 'updated')

@admin.register(EWallet)
class EWalletAdmin(admin.ModelAdmin):
    model=EWallet
    list_display = ['user', 'e_wallet_name', 'account_email', 'valid']
    list_filter = ['user', 'valid']
    search_fields = ['user__username', 'e_wallet_name', 'account_email']
    prepopulated_fields = {'slug': ('account_email',)}
    readonly_fields = ['created', 'updated']
    fieldsets = (
        ('General Information', {
            'fields': ('user', 'e_wallet_name', 'account_email', 'valid', 'slug')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_type', 'name_on_card', 'card_number', 'expiration_date', 'cvv', 'valid']
    list_filter = ['user', 'card_type', 'valid']
    search_fields = ['user__username', 'name_on_card', 'card_number']
    readonly_fields = ['created', 'updated']

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = unique_slug(f"{obj.user.username}-{obj.method_type}")
        super().save_model(request, obj, form, change)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    model=BankAccount
    list_display = ['user', 'account_number', 'routing_number', 'validity', 'created', 'updated']
    search_fields = ['user__username', 'account_number', 'routing_number']
    readonly_fields = ['created', 'updated']
    
    def save_model(self, request, obj, form, change):
        # Automatically generate slug based on the user's username
        if not obj.slug:
            obj.slug = unique_slug(f"{obj.method_type} {obj.user.username}")
        super().save_model(request, obj, form, change)

#RidePreference
@admin.register(RidePreference)
class RidePreferenceAdmin(admin.ModelAdmin):
    model = RidePreference
    list_display = ['user','ride_preference','slug','created','updated']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()

#TaxDocumentSetting
@admin.register(TaxDocumentSetting)
class TaxDocumentSettingAdmin(admin.ModelAdmin):
    model = TaxDocumentSetting
    list_display = ('user', 'taxUserType', 'formType', 'states', 'slug', 'created','updated')
    list_filter = ('taxUserType', 'formType', 'states', 'created', 'updated')
    search_fields = ('user__username', 'taxUserType', 'formType')
    readonly_fields = ['slug' , 'created', 'updated']

