from django.contrib import admin
from .models import Testimonial



@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = ['author', 'video_url', 'description', 'created_at', 'updated_at', 'views_count']
   

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return ('created_at', 'updated_at')
        return ()
