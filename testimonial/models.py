      
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Testimonial(models.Model):
    title = models.CharField(max_length=255 ,blank=True, null=True)
    image = models.ImageField(upload_to="logo_image/%Y/%m/%d" ,blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=500,blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse("testimonial:testimonial_list", kwargs={"pk": self.pk})
    