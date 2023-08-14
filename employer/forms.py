from django import forms
from .models import CompanyProfile

class CompanyProfileCreateForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'company_name', 'logo', 'headquarters_address', 'city', 'state', 'country', 'zip_code',
            'employees', 'industry', 'description', 'video', 'representative_full_name', 'Department',
            'telephone', 'website', 'email', 'fax', 'opening_hours', 'google_map_link',
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'headquarters_address': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'state': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'country': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'employees': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'industry': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
            'representative_full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'Department': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'website': forms.URLInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'fax': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'google_map_link': forms.URLInput(attrs={'class': 'form-control form-control-sm'}),
        }

   
