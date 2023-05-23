from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
#from .models import Policies, UserAcceptedPolicies
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect
from django.views import View

class DashboardInformation(LoginRequiredMixin, View):
    template_name = 'supperAdmin/dashboardInfo.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)