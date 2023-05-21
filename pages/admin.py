from django.contrib import admin
from .models import MyEmptyModel
class MyEmptyAppAdmin(admin.ModelAdmin):
    # Customize the admin view for your app if needed
    pass
# Register your app in the admin interface
admin.site.register(MyEmptyModel, MyEmptyAppAdmin)


