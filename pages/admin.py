from django.contrib import admin
from .models import MyEmptyModel, Subscriber
class MyEmptyAppAdmin(admin.ModelAdmin):
    # Customize the admin view for your app if needed
    pass
# Register your app in the admin interface
admin.site.register(MyEmptyModel, MyEmptyAppAdmin)


class SubscriberAppAdmin(admin.ModelAdmin):
    list_display =['email','created']
    
admin.site.register(Subscriber, SubscriberAppAdmin)