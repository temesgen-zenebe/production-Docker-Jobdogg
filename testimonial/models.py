from django.db import models

class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    video_url = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.author
        
