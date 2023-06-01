from django import forms
from datetime import datetime
from .models import Personal, Language, BasicInformation
from django.utils.safestring import mark_safe


class PersonalForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.SelectMultiple,
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['languages'].widget.choices = self.fields['languages'].choices # Update the queryset for the 'languages' field
        self.user = user
            
    class Meta:
        model = Personal
        fields = (
            'nickname',
            'social_security_number',
            'drivers_license_number',
            'drivers_license_state',
            'date_of_birth',
            'gender',
            'languages',
            'e_verify',
        )
        widgets = {
            'drivers_license_state': forms.Select(attrs={'class': 'select form-select form-control form-control-sm'}),
            'gender': forms.Select(attrs={'class': 'select form-select form-control form-control-sm'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date','style': 'width: 100%; font-size:13px;'}), 
        }
        


class BasicInformationForm(forms.ModelForm):
    class Meta:
        model = BasicInformation
        fields = (
            'address',
            'apartment',
            'city',
            'state',
            'zip_code',
            'cell_phone',
            'home_phone',
            'work_phone',
            'email',
            'emergency_contact_number',
            'emergency_contact_name',
        )
        widgets = {
            'address': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm', 'placeholder': '1234 Main St'}),
            'apartment': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm', 'placeholder': '#100'}),
            'city': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm '}),
            'state': forms.Select(attrs={'class': 'select form-select form-control form-control-sm'}),
            'zip_code': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm'}),
            'cell_phone': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm'}),
            'home_phone': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm'}),
            'work_phone': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'emailinput form-control form-control-sm'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm'}),
        }
       