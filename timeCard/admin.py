from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DateAssigned, TimeAssigned, TimeCard

#TimeAssigned
@admin.register(TimeAssigned)
class TimeAssignedAdmin(admin.ModelAdmin):
    model = TimeAssigned
    list_display = ('title','start_time', 'end_time', 'total_hours', 'slug', 'created', 'updated')
    search_fields = ['start_time', 'end_time', 'slug']
    list_filter = ['created', 'updated']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
    
    
@admin.register(DateAssigned)   
class DateAssignedAdmin(admin.ModelAdmin):
    model=DateAssigned
    list_display = ('date_assign', 'time_assign', 'slug', 'created', 'updated')
    search_fields = ['date_assign', 'slug']
    list_filter = ['created', 'updated']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()

@admin.register(TimeCard)
class TimeCardAdmin(admin.ModelAdmin):
    model=TimeCard
    list_display = ('employer', 'employee', 'date_assigned', 'job_type', 'location_URL', 'slug', 'created', 'updated')
    search_fields = ['employer', 'employee', 'slug']
    list_filter = ['created', 'updated']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()