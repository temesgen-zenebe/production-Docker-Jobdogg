from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group
from django.conf import settings
import stripe
import paypalrestsdk
from common.utils.email import send_email
from django.core.mail import send_mail
import uuid

User = settings.AUTH_USER_MODEL

class DashboardInformation(LoginRequiredMixin, View):
    template_name = 'employer/dashboardInfo.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
    

class BeEmployerRequestView(LoginRequiredMixin, View):
    
    
    def get(self, request):
        context = {}
        return render(request, 'employer/be_employer_request.html', context)
    
    def post(self, request):
        
        # Send email request to the system using SendGrid
        activation_key = str(uuid.uuid4())  # Generate a unique activation key
        activation_link = request.build_absolute_uri(reverse('employer:activate_employer')) 

        message = f"Click the following link to activate your employer account:\n{activation_link}"
        send_mail(
            subject='Activate Your Employer Account',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        return redirect('employer:vilificationSandMassage')
       
   
class ActivateEmployerView(LoginRequiredMixin, View):
    def get(self, request):
        # Update user group to "is_employer" and activate the account
        user = request.user
        current_group = user.groups.first()
        employer_group = Group.objects.get(name='employer')
        employee_group = Group.objects.get(name='employee')

        if  current_group and current_group.name == 'employee':
            user.groups.remove(current_group)
            user.groups.add(employer_group)
            user.is_active = True
            user.save()
        else :
            user.groups.add(employer_group)
            user.is_active = True
            user.save()
           
        return redirect('employer:dashboard_information_employer')  # Replace 'dashboard' with the actual URL name of the user's dashboard


class VilificationSandMassage(TemplateView):
    template_name = 'employer/verification.html'