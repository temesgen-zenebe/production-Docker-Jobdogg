from django.contrib import admin
from common.utils.text import unique_slug
from .models import CompanyProfile, ProfileBuildingController

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

