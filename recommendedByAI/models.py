from django.db import models
from common.utils.text import unique_slug

from employee.models import EmployeePreferences
from employer.models import JobRequisition

#RecommendedJobs
class RecommendedJobs(models.Model):
    employee_preferences = models.ForeignKey(EmployeePreferences, on_delete=models.CASCADE)
    job_requisition = models.ForeignKey(JobRequisition, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    
    @property
    def user(self):
        return self.employee_preferences.user

    def save(self, *args, **kwargs):
        if not self.slug:
            value = f"{self.employee_preferences.user.username}"
            self.slug = unique_slug(value, type(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_preferences.user.username}"