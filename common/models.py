from django.db import models
from django.conf import settings

from common.utils.text import unique_slug

# Create your models here.
class ProfileBuildingControler(models.Model):
    account_created = models.BooleanField(default=False)
    companyProfile_created = models.BooleanField(default=False)
    paymentInformation_created = models.BooleanField(default=False)
    policeAccepted_created = models.BooleanField(default=False)
    contractSigned_created = models.BooleanField(default=False)
    paymentPlane_validate = models.BooleanField(default=False)
    billingInformation_created = models.BooleanField(default=False)
    

class CompanyProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    founded_date = models.DateField()
    headquarters_address = models.CharField(max_length=200)
    representative_name = models.CharField(max_length=100)
    email = models.EmailField()
    employees = models.PositiveIntegerField(blank=True,null=True)
    industry = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.company_name} {self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    