from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DateAssigned, TimeAssigned, TimeCard,ClockOutClockInManagement

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
 

@admin.register(ClockOutClockInManagement)  
class ClockOutClockInManagementAdmin(admin.ModelAdmin):
    model= ClockOutClockInManagement
    list_display = ('time_card', 'clock_in', 'clock_in_time', 'clock_out', 'clock_out_time', 'total_clock_in_out_hours',
                    'over_time_clock_in', 'over_time_clock_in_time', 'over_time_clock_out', 'over_time_clock_out_time', 'total_over_time_clock_in_out_hours',
                    'break_in', 'break_in_time', 'break_out', 'break_out_time', 'total_break_in_out_hours',
                    'sick', 'no_show', 'net_working_hour', 'employee_conformation', 'employer_conformation', 'slug', 'created', 'updated')

    search_fields = ['time_card__employee', 'time_card__employer', 'slug']
    list_filter = ['clock_in', 'clock_out', 'over_time_clock_in', 'over_time_clock_out', 'break_in', 'break_out', 'sick', 'no_show',
                   'employee_conformation', 'employer_conformation', 'created', 'updated']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('created', 'updated', 'slug')
        return ()
    