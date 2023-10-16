from django.views.generic import TemplateView,ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render,redirect
from users.templatetags.user_tags import is_admin, is_employee, is_employer
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Subscriber
from .forms import SubscribeForm
import logging

class HomePageView(TemplateView):
    template_name = 'pages/home.html'
    
    def get(self, request):
        context={ 'form':SubscribeForm() }
        return render(request, self.template_name, context)

    def post(self, request):
        if 'subscribe' in request.POST:
            sub_form = SubscribeForm(request.POST)
            if sub_form .is_valid():
               experience = sub_form .save(commit=False)
               experience.save()
               messages.success(self.request, 'Thank you for subscribing!')
               return redirect('pages:homepage')
            else:
              print("Subscribe Form email form is invalid")
              
        context={ 'form':SubscribeForm() }
        return render(request, self.template_name, context)

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
    
class ExecutiveTeam(TemplateView):
    template_name = 'pages/executive_team.html'

class HowItWoksForEmployee(TemplateView):
    template_name = 'pages/HowItWoks-ForEmployee.html'
class HowItWoksForEmployer(TemplateView):
    template_name = 'pages/HowItWoks-ForEmployer.html'   

class EmployeeFAQ(TemplateView):
    template_name = 'pages/employee_FAQ.html' 

class EmployerFAQ(TemplateView):
    template_name = 'pages/employer_FAQ.html'
    
class TermsAndPolicy(TemplateView):
    template_name = 'pages/termsAndPolicy.html'
   
class BlogView(TemplateView):
    template_name = 'pages/blog.html'
    
#OurDoggsView, 
class OurDoggsView(TemplateView):
    template_name = 'pages/ourDoggs.html'
    
#GetStaffView, 
class GetStaffView(TemplateView):
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


# def redirect_to_homepage(request):
   
#     if request.user.is_authenticated:
#         if is_admin(request.user): # Admin
#             return redirect('pages:adminHomePage')
#         elif is_employee(request.user):  # Employee (Assuming you have a custom user model with an 'is_employee' field)
#             return redirect('pages:employeeHomePage')
#         elif is_employer(request.user):  # Employer (Assuming you have a custom user model with an 'is_employer' field)
#             return redirect('pages:employerHomePage')

#     # Default fallback if no matching role is found
#     return redirect('pages:employeeHomePage')  # You can set the default to any page you prefer


def redirect_to_homepage(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            logging.info("User is an admin")
            return redirect('pages:adminHomePage')
        elif is_employee(request.user):
            logging.info("User is an employee")
            return redirect('pages:employeeHomePage')
        elif is_employer(request.user):
            logging.info("User is an employer")
            return redirect('pages:employerHomePage')

    logging.warning("No matching role found, defaulting to employeeHomePage")
    return redirect('pages:employeeHomePage')




class SubscriberListView(ListView):
    model = Subscriber
    template_name = 'pages/home.html'
    context_object_name = 'subscribers'

class SubscriberCreateView(CreateView):
    model = Subscriber
    form_class = SubscribeForm
    template_name = 'subscriptingForNewsLetter/subscriber_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Thank you for subscribing!')
        return response

class SubscriberUpdateView(UpdateView):
    model = Subscriber
    form_class = SubscribeForm
    template_name = 'subscriptingForNewsLetter/subscriber_form.html'

class SubscriberDeleteView(DeleteView):
    model = Subscriber
    template_name = 'subscriptingForNewsLetter/subscriber_confirm_delete.html'
    success_url = reverse_lazy('subscriber_list')
