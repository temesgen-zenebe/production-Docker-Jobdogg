from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = [
        'title',
        'image', 
        'video_url', 
        'description',
        'author',
        'target_audience',
        'created_at', 
        'updated_at', 
        'view_count',
    ]
   

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created_at', 'updated_at')
        return ()
