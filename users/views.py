from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from django.shortcuts import redirect
from allauth.account.views import PasswordChangeView
from .forms import CustomUserChangeForm
from django.conf import settings 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.views import View
from django.dispatch import Signal
from django.contrib.auth import get_user_model

User=get_user_model()

CustomUser = settings.AUTH_USER_MODEL

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('my-account')
    

class MyAccountPageView(SuccessMessageMixin,LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'account/my_account.html'
    success_message = 'Update Successful'

    def get_object(self):
        return self.request.user


    

