from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render,redirect
from users.templatetags.user_tags import is_admin, is_employee, is_employer
from django.contrib.auth.decorators import login_required

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
 
class BlogView(TemplateView):
    template_name = 'pages/blog.html'
    
#OurDoggsView, 
class OurDoggsView(TemplateView):
    template_name = 'pages/ourDoggs.html'
    
#GetStaffView, 
class                 GetStaffView(TemplateView):
    template_name = 'pages/getStaff.html'
    
#GetWorkView
class GetWorkView(TemplateView):
    template_name = 'pages/getWork.html'
    

def dashboard(request):
    if request.user.is_authenticated and is_admin(request.user):
        return render(request, 'pages/supperAdmin_dashboard.html')
    elif request.user.is_authenticated and is_employee(request.user):
        return render(request, 'pages/employee_dashboard.html')
    elif request.user.is_authenticated and is_employer(request.user):
        return render(request, 'pages/employer_dashboard.html')
    else:
        return redirect('login')


@login_required
def employee_home(request):
    # Your code for employee homepage view
    return render(request, 'pages/employee_home.html')

@login_required
def employer_home(request):
    # Your code for employer homepage view
    return render(request, 'pages/employer_home.html')

@login_required
def admin_home(request):
    # Your code for admin homepage view
    return render(request, 'pages/admin_home.html')


def redirect_to_homepage(request):
   
    if request.user.is_authenticated:
        if is_admin(request.user): # Admin
            return redirect('pages:adminHomePage')
        elif is_employee(request.user):  # Employee (Assuming you have a custom user model with an 'is_employee' field)
            return redirect('pages:employeeHomePage')
        elif is_employer(request.user):  # Employer (Assuming you have a custom user model with an 'is_employer' field)
            return redirect('pages:employerHomePage')

    # Default fallback if no matching role is found
    return redirect('pages:employeeHomePage')  # You can set the default to any page you prefer
