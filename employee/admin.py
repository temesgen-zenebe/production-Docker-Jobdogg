from django.contrib import admin
from .models import (
      Policies, UserAcceptedPolicies,BasicInformation
    )

    
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
    'state', 
    'zip_code',
    'cell_phone',
    'home_phone',
    'work_phone',
    'email',
    'city',
    'emergency_contact_number', 
    'emergency_contact_name',
    'created', 
    'updated'
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
  
   