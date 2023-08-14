from django.db import models
from django.utils.timezone import datetime
from django.conf import settings
from common.utils.text import unique_slug
from localflavor.us.models import USStateField 

# Create your models here.
class ProfileBuildingController(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_account_created = models.BooleanField(default=False)
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

    