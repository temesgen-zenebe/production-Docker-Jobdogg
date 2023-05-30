from datetime import datetime
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import DateInput
from django import forms
from .models import CustomUser
from django.contrib.auth.models import Group



BIRTH_YEAR_CHOICES = range(1915, datetime.now().year)

class SignupForm(forms.Form):
   
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    # Other form fields...

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type'] 
        
        if user.user_type == 'employee':
            group = Group.objects.get(name='employee')
        elif user.user_type == 'employer':
            group = Group.objects.get(name='employer')
        else:
            pass
            # Handle the case when the user_type is neither employee nor employer
            # This is optional based on your requirements
        user.save()
        group.user_set.add(user)
            
class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'dob', 'avatar')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'dob': DateInput(attrs={'type': 'date','style': 'width: 100%; font-size:13px;'}), 
           
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),
        }
        
        """class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name', 'dob', 'avatar')
        widgets = {
            'dob': forms.SelectDateWidget(
                attrs={
                    'style': 'width: 31%; display: inline-block; margin: 0 1%'
                },
                years = BIRTH_YEAR_CHOICES
            )
        }"""

