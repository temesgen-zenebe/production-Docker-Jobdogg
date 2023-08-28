from django.contrib import admin
from recommendedByAI.models import AppliedJobHistory, RecommendedJobs

@admin.register(RecommendedJobs)
class RecommendedJobsAdmin(admin.ModelAdmin):
    model=RecommendedJobs
    list_display = ('employee_preferences', 'job_requisition', 'slug', 'created')  
    
@admin.register(AppliedJobHistory)
class AppliedJobHistoryAdmin(admin.ModelAdmin):
    model=AppliedJobHistory
    list_display = ('user' ,'job' ,'applied_date', 'status', 'message','slug','created','updated' )