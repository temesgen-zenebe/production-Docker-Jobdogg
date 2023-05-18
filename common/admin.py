from django.contrib import admin

# Register your models here.
admin.site.index_title = 'Home'
admin.site.site_title = 'Jobdogg Admin'
admin.site.site_header = 'Jobdogg Admin'


class DjangoJokesAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_max_show_all = 1000
    save_as = True