from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render,redirect
from users.templatetags.user_tags import is_admin, is_employee, is_employer

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutUsView(TemplateView):
    template_name = 'pages/about_us.html'

    def get(self, request, *args, **kwargs):
        messages.debug(request, 'Debug message.')
        messages.info(request, 'Info message.')
        messages.success(request, 'Success message.')
        messages.warning(request, 'Warning message.')
        messages.error(request, 'Error message.')
        return super().get(request, args, kwargs)
    
class ContactUsView(TemplateView):
    template_name = 'pages/contact_us.html'


def dashboard(request):
    if request.user.is_authenticated and is_admin(request.user):
        return render(request, 'pages/admin_dashboard.html')
    elif request.user.is_authenticated and is_employee(request.user):
        return render(request, 'pages/employee_dashboard.html')
    elif request.user.is_authenticated and is_employer(request.user):
        return render(request, 'pages/employer_dashboard.html')
    else:
        return redirect('login')




    