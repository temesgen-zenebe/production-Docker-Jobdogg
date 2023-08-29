from django.contrib import admin
from JobFilter.models import AppliedSearchJobHistory

@admin.register(AppliedSearchJobHistory)
class AppliedSearchJobHistoryAdmin(admin.ModelAdmin):
    model=AppliedSearchJobHistory
    list_display = ('user' ,'Search_job' ,'applied_date', 'status', 'message','slug','created','updated',)