
from django.db import models
from common.utils.chooseConstant import DATE_ASSIGN
from common.utils.text import unique_slug
from jobDoggApp import settings
from datetime import datetime
from django.utils import timezone

class TimeAssigned(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    lunch_time = models.TimeField(null=True, blank=True)
    over_start_time = models.TimeField(null=True, blank=True)
    over_end_time = models.TimeField(null=True, blank=True)
    total_over_time = models.IntegerField()
    double_over_time = models.IntegerField(null=True, blank=True)
    total_hours = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"card-time-{self.start_time}"
            self.slug = unique_slug(value, type(self))
        
        if self.over_start_time and self.over_end_time:
            start_time = datetime.combine(datetime.today(), self.over_start_time)
            end_time = datetime.combine(datetime.today(), self.over_end_time)
            over_time = end_time - start_time
            self.total_over_time = over_time.total_seconds() // 60  # Convert to minutes
            
            # Calculate total hours
            start_datetime = datetime.combine(datetime.today(), self.start_time)
            end_datetime = datetime.combine(datetime.today(), self.end_time)
            total_time = end_datetime - start_datetime
            total_minutes = total_time.total_seconds() // 60  # Convert to minutes
            self.total_hours = total_minutes + self.total_over_time
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title}-start:{self.start_time}-end:{self.end_time}"
  
class DateAssigned(models.Model):
    date_assign = models.CharField(choices=DATE_ASSIGN)
    time_assign = models.ForeignKey(TimeAssigned, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.date_assign}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.date_assign}-{self.time_assign}"
    
class TimeCard(models.Model):
    employer=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee = models.CharField(max_length=100, default='Temesgen')
    date_assigned = models.ForeignKey(DateAssigned, on_delete=models.CASCADE)
    job_type = models.CharField(default='Temporary')
    location_URL = models.URLField(
        max_length=200, null=True, blank=True, 
        help_text='Enter the google maps link for the business location'
    )
    
    special_task = models.TextField(max_length=200, null=True, blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.employee}-{self.employer}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"From {self.employer}-to-{self.employee}'s timeCards"
    
    
class ClockOutClockInManagement(models.Model):
    time_card = models.ForeignKey(TimeCard, on_delete=models.CASCADE)
    
    employee_in=models.BooleanField(default=False)
    employee_in_time = models.DateTimeField()
    
    employee_out=models.BooleanField(default=False)
    employee_out_time = models.DateTimeField(auto_now=True)
    
    employee_conformation=models.BooleanField(default=False)
    employer_conformation=models.BooleanField(default=False)
    sick = models.BooleanField(default=False)
    no_show = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.time_card.employee}-{self.time_card.employer}"
            self.slug = unique_slug(value, type(self))
        if  self.employee_in :
            self.employee_in_time = timezone.now()
        if self.employee_out :
            self.employee_out_time = timezone.now()   
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.time_card.employee}-{self.time_card.employer}-clock-out-clock-in-management"