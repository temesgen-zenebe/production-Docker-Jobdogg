from django import forms
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import datetime
import os
import moviepy.editor as mp

from .models import (
    Background_Check, Category, CertificationLicense, 
    Education, EmployeePreferences, 
    Experience, Military, Personal, 
    Language, BasicInformation, 
    Position, SafetyTestResult, 
    Skill, RettingCommenting, VideoResume,
)
from django.utils.safestring import mark_safe
from common.utils.chooseConstant import DISCHARGE_YEAR_CHOICES
from .models import UserAcceptedPolicies

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import VideoResume

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
        user = kwargs.pop('user', None)  # Remove the 'user' argument from kwargs
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
        labels = {
            'can_relocation': 'Are you willing to relocate?',
            'years_of_experience': 'Years of experience'
            # Add labels for other fields here
        }
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
        
#SafetyTestResultForm      
class SafetyTestResultForm(forms.ModelForm):
    class Meta:
        model = SafetyTestResult
        fields = ['safety_result', 'states']
        widgets = {
            'safety_result': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm', 'id': 'id_safety_result', 'type': 'hidden'}),
            'states': forms.TextInput(attrs={'class': 'textinput form-control form-control-sm', 'id': 'id_states', 'type': 'hidden'}),
        }
        
#VideoResumeForm
class VideoResumeForm(forms.ModelForm):
    class Meta:
        model = VideoResume
        fields = ['video','tell_about_you']
        labels = {
            'video': 'Upload Video',
            'tell_about_you': 'Share a fascinating fact or story about yourself',
        }
        widgets = {
            'video': forms.ClearableFileInput(attrs={'accept': ','.join(settings.ALLOWED_VIDEO_EXTENSIONS), 'class': 'textinput form-control form-control-sm'}),
            'tell_about_you': forms.Textarea(attrs={'rows': 4,'class': 'textinput form-control form-control-sm'}),
        }

    def clean_video1(self):
        video = self.cleaned_data.get('video')
        if video:
            if not video.name.lower().endswith(tuple(settings.ALLOWED_VIDEO_EXTENSIONS)):
                raise ValidationError(_('Invalid video format. Supported formats are: {}').format(', '.join(settings.ALLOWED_VIDEO_EXTENSIONS)))

            duration = self.get_video_duration(video)
            if duration > settings.MAX_VIDEO_DURATION:
                raise ValidationError(_('Maximum video duration exceeded. Please upload a video with a maximum duration of 1 minutes.'))
        
        return video
    
    def clean_video(self):
        video = self.cleaned_data.get('video')
        duration = self.cleaned_data.get('duration')

        if video and duration is not None and duration > 2:
            # Trim the video duration to 1 minutes
            # Add your logic here to trim the video duration to the desired length
            if not video.name.lower().endswith(tuple(settings.ALLOWED_VIDEO_EXTENSIONS)):
                raise ValidationError(_('Invalid video format. Supported formats are: {}').format(', '.join(settings.ALLOWED_VIDEO_EXTENSIONS)))

            duration = self.get_video_duration(video)
            if duration > settings.MAX_VIDEO_DURATION:
                raise ValidationError(_('Maximum video duration exceeded. Please upload a video with a maximum duration of 1 minutes.'))
        return video

    def get_video_duration(self, video_file):
        try:
            # Get the temporary file path
            temp_file_path = video_file.temporary_file_path()

            # Use moviepy to get the video duration
            video = mp.VideoFileClip(temp_file_path)
            duration = video.duration

            # Clean up the temporary file
            os.remove(temp_file_path)

            return duration
        except Exception as e:
            # Handle any exceptions
            print(f"Error retrieving video duration: {str(e)}")
            return None


#BackgroundCheckForm


class BackgroundCheckForm(forms.ModelForm):
    class Meta:
        model = Background_Check
        fields = ['certification_file', 'expiration_date']
        widgets = {
            'certification_file': forms.FileInput(attrs={'class': 'form-control form-control-sm','type': 'hidden'}),
            'expiration_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-sm', 'type': 'hidden'}),
        }
class BackgroundCheckFormUpdate(forms.ModelForm):
    class Meta:
        model = Background_Check
        fields = ['certification_file', 'expiration_date']
        widgets = {
            'certification_file': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'expiration_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-sm'}),
        }