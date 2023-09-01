from audioop import reverse
from django.db import models
from django.core.cache import cache
from django.utils.timezone import datetime
from django.conf import settings
from common.utils.chooseConstant import (
    ACTION_TYPES, DEGREE_TYPE_CHOICES, 
    JOB_TYPES, RELOCATION, SALARY_TYPES, 
    WORK_ARRANGEMENT_CHOICES
)
from common.utils.text import unique_slug
from localflavor.us.models import USStateField

from employee.models import Category, Position, Skill 

# Create your models here.
class ProfileBuildingController(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_account_created = models.BooleanField(default=True)
    is_company_profile_created = models.BooleanField(default=False)
    is_payment_information_created = models.BooleanField(default=False)
    is_police_accepted_created = models.BooleanField(default=False)
    is_contract_signed_created = models.BooleanField(default=False)
    is_payment_plan_validated = models.BooleanField(default=False)
    is_billing_information_created = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile Building Controller"
    

class CompanyProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    headquarters_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50, default="city")
    state =  USStateField(default="CA")
    country = models.CharField(max_length=50, default="country")
    zip_code = models.CharField(max_length=10, default='zip')
    employees = models.PositiveIntegerField(blank=True, null=True)
    industry = models.CharField(max_length=50)
    description = models.TextField(max_length=300, blank=True, null=True, help_text="Short description about your company.")
    video = models.FileField(upload_to='company_profile_video/%Y/%m/%d', blank=True, null=True)
    representative_full_name = models.CharField(max_length=100)
    Department = models.CharField(max_length=100,blank=True, null=True)
    telephone = models.CharField(max_length=20, default="phone")
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(max_length=100)
    fax = models.CharField(max_length=20, null=True, blank=True)
    opening_hours = models.CharField(
        max_length=200, null=True, blank=True,
        help_text="Enter opening hours in the format: 'Weekend Hours (Mon-Fri 9:00 AM - 5:00 PM)' and 'Weekday Hours (Sat-Sun 3:00 AM - 2:00 PM).'"
    )
    google_map_link = models.URLField(
        max_length=200,null=True, blank=True,
        help_text="Enter the Google Maps link for your location."
    )
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.company_name} {self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

#EmployerPolicies
class EmployerPoliciesAndTerms(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title 

#EmployerAcceptedPolicies  
class EmployerAcceptedPolicies(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    policies = models.ForeignKey(EmployerPoliciesAndTerms, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, editable=False)

    def __str__(self):
        return str(f'{self.policies}-{self.accepted}')

    def save(self, *args, **kwargs):
        if not self.slug:
            value = str(self)
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)    
        
class SocCode(models.Model):
    soc_code = models.CharField(max_length=200)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='soc_code')
    
    def __str__(self):
        return f'{self.soc_code}'
     
class JobRequisition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    industry = models.ForeignKey(Category, on_delete=models.CASCADE)
    job_title= models.ManyToManyField(Position, related_name='jobTitle') 
    custom_job_title = models.CharField(max_length=200, null=True, blank=True)
    required_skills = models.ManyToManyField(Skill)
    custom_required_skills = models.TextField(max_length=200, null=True, blank=True)
    soc_code = models.CharField(max_length=100, default='0000', null=True, blank=True)
    department = models.CharField(max_length=255)
    min_experience = models.PositiveIntegerField()
    min_degree_requirements = models.CharField(max_length=100 , choices=DEGREE_TYPE_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    salary_type = models.CharField(max_length=20, choices=SALARY_TYPES)
    min_salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    work_arrangement_preference = models.CharField(
        max_length=10,choices=WORK_ARRANGEMENT_CHOICES,default='REMOTE')
    relocatable = models.CharField(max_length=10, choices=RELOCATION)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    address1 = models.CharField(max_length=255)
    certifications_required = models.TextField(blank=True)
    star_rating = models.PositiveIntegerField()
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    from_date = models.DateField()
    to_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    job_description = models.TextField()
    number_views = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=True)
    preference_action = models.CharField(max_length=20, choices=ACTION_TYPES, default="ALL")
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    


    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.job_type} {self.user.username}"
            self.slug = unique_slug(value, type(self))

        super().save(*args, **kwargs)  # Save the object
    
    def get_absolute_url(self):
        return reverse('employer:job_requisition_detail', kwargs={'slug': self.slug})
        
    def __str__(self):
        return f"{self.user.username}-Job Requisition {self.pk}"
    
    
    @property
    def job_title_cache_key(self):
        return f"employer_job_title_{self.industry_id}"

    @property
    def required_skills_cache_key(self):
        return f"employer_required_skills_{self.job_title.values_list('id', flat=True)}"
    
    
    def get_job_title(self):
        positions = cache.get(self.job_title_cache_key)
        if not positions:
            positions = Position.objects.filter(category=self.industry)
            cache.set(self.job_title_cache_key, positions)
        return positions

    def get_skills(self):
        skills = cache.get(self.required_skills_cache_key)
        if not skills:
            skills = Skill.objects.filter(position__in=self.job_title.all())
            cache.set(self.required_skills_cache_key, skills)
            print(skills)
        return skills
    
class TimeCard(models.Model):
    employer=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee=models.CharField(max_length=100)
    date=models.DateTimeField()
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    massage = models.TextField(max_length=200,null=True, blank=True)
    google_map_link = models.URLField(
        max_length=200,null=True, blank=True,
        help_text="Enter the Google Maps link for your location."
    )
    task=models.CharField(max_length=100,null=True, blank=True)
    employee_conformation=models.BooleanField(default=False)
    employer_conformation=models.BooleanField(default=False)
    slug=models.SlugField(unique=True)
    spacial_discretion = models.TextField(max_length=200)
    incentive = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.employee}"
            self.slug = unique_slug(value, type(self))

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee}'s Preferences"