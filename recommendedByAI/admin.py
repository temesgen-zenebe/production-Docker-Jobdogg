from django.contrib import admin
from recommendedByAI.models import RecommendedJobs

@admin.register(RecommendedJobs)
class RecommendedJobsAdmin(admin.ModelAdmin):
    model=RecommendedJobs
    list_display = ('employee_preferences', 'job_requisition', 'slug', 'created')  