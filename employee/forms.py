from django import forms
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Category, CertificationLicense, Education, EmployeePreferences, Experience, Military, Personal, Language, BasicInformation, Position, Skill
from django.utils.safestring import mark_safe
from common.utils.chooseConstant import DISCHARGE_YEAR_CHOICES
from .models import UserAcceptedPolicies

class UserAcceptedPoliciesForm(forms.ModelForm):
    class Meta:
        model = UserAcceptedPolicies
        fields = ['policies']
        
class MultiSelectDropdown(forms.SelectMultiple):
    def value_from_datadict(self, data, files, name):
        if isinstance(data, (list, tuple)):
            return [int(value) for value in data]
        return [int(value) for value in data.getlist(name, [])]

class PersonalForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=MultiSelectDropdown(attrs={'class': 'multiselect'}),
        help_text="Select multiple options by holding down the Ctrl key (or Command key on Mac)."
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
       
       
class MilitaryForm(forms.ModelForm):
    certification_license = forms.FileField(
        required=False,  # Make the field optional
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = Military
        fields = ['branch', 'rank', 'discharge_year', 'duty_flag', 'certification_license']
        widgets = {
            'branch': forms.Select(attrs={'class': 'select form-select form-control form-control-sm'}),
            'rank': forms.Select(attrs={'class': 'select form-select form-control form-control-sm'}),
            'discharge_year': forms.DateInput(attrs={'type': 'date','style': 'width: 100%; font-size:13px;'}), 
            'duty_flag': forms.Select(attrs={'class': 'select form-select form-control form-control-sm'}),
            #'certification_license': forms.ClearableFileInput(attrs={'multiple': True}),
        
        }
        
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('school_type', 'school_name', 'country', 'city', 'state', 'graduated', 'graduation_date', 'degree_type')
        widgets = {
            'graduation_date': forms.DateInput(attrs={'type': 'date','style': 'width: 100%; font-size:13px;'})
        }


class CertificationLicenseForm(forms.ModelForm):
    class Meta:
        model = CertificationLicense
        fields = ['document_name', 'certification_file']
        
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_name', 'company_phone', 'job_title', 'start_date','is_current', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class EmployeePreferencesForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'id_category'})
    )
    desired_positions = forms.ModelChoiceField(
        queryset=Position.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'id_desired_positions'})
    )
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control form-control-sm', 'id': 'id_skills'}),
        help_text="Select multiple options by holding down the Ctrl key (or Command key on Mac)."
    )
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['desired_positions'].queryset = Position.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass  # Invalid category ID, handle it accordingly

        if 'desired_positions' in self.data:
            try:
                desired_positions_ids = map(int, self.data.getlist('desired_positions'))
                self.fields['skills'].queryset = Skill.objects.filter(position__in=desired_positions_ids)
            except (ValueError, TypeError):
                pass  # Invalid desired_positions IDs, handle it accordingly

    class Meta:
        model = EmployeePreferences
        fields = [
            'minimum_salary',
            'salary_type',
            'location',
            'can_relocation',
            'job_type',
            'years_of_experience',
            'custom_positions',
            'custom_skills'
        ]
        widgets = {
            'minimum_salary': forms.NumberInput(attrs={'class': 'numberinput form-control form-control-sm', 'id': 'id_minimum_salary'}),
            'salary_type': forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_salary_type'}),
            'location': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm', 'id': 'id_location'}),
            'can_relocation': forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_can_relocation','placeholder':'select'}),
            'job_type': forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_job_type'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'numberinput form-control form-control-sm', 'id': 'id_years_of_experience'}),
            'custom_positions': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm', 'id': 'id_custom_positions'}),
            'custom_skills': forms.Textarea(attrs={'class': 'textarea form-control form-control-sm', 'id': 'id_custom_skills'}),
        }
