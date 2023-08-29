from django.db import models
from common.utils.chooseConstant import STATUS_CHOICES
from common.utils.text import unique_slug
from employer.models import JobRequisition
from jobDoggApp import settings


#AppliedJobHistory
class AppliedSearchJobHistory(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Search_job = models.ForeignKey(JobRequisition, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    message = models.TextField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.Search_job}"