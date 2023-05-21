from django.contrib import admin
from .models import (
      Policies, UserAcceptedPolicies
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
    