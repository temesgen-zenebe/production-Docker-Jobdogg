from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import datetime
import os
import moviepy.editor as mp

from .models import (
    Background_Check, BankAccount, Card, Category, CertificationLicense, CheckByEmail, EWallet, 
    Education, EmployeePreferences, 
    Experience, Military, Personal, 
    Language, BasicInformation, 
    Position, RidePreference, SafetyTestResult, 
    Skill, RettingCommenting, TaxDocumentSetting, VideoResume,
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
        help_texts = {
            'social_security_number': 'Enter in this format XXX-XX-XXXX',
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
        
        fields = (
                'minimum_salary','salary_type', 'job_type', 'location',
                'work_arrangement_preference', 'can_relocation', 
                'years_of_experience','custom_positions','custom_skills'
                )
        labels = {
            'can_relocation': 'Are you willing to relocate?',
            'years_of_experience': 'Years of experience'
            # Add labels for other fields here
        }
        widgets = {
            'minimum_salary': forms.NumberInput(attrs={'class': 'numberinput form-control form-control-sm', 'id': 'id_minimum_salary'}),
            'salary_type': forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_salary_type'}),
            'job_type': forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_job_type'}),
            'location': forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_location'}),
            'work_arrangement_preference':forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_work_arrangement_preference'}),
            'can_relocation': forms.Select(attrs={'class': 'select form-select form-select-sm', 'id': 'id_can_relocation','placeholder':'select'}),
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
            'certification_file': forms.FileInput(attrs={'class': 'form-control form-control-sm', 'style': 'display: none;'}),
            'expiration_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-sm', 'style': 'display: none;'}),
        }
             
class BackgroundCheckFormUpdate(forms.ModelForm):
    class Meta:
        model = Background_Check
        fields = ['certification_file', 'expiration_date']
        widgets = {
            'certification_file': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'expiration_date': forms.DateTimeInput(attrs={'class': 'form-control form-control-sm'}),
        }
        
#Payment Preference
class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_number', 'routing_number']
        widgets = {
            'account_number': forms.TextInput(
                attrs={
                    'pattern': '^[0-9]{6,20}$',
                    'maxlength': '20', 
                    'minlength': '6',
                    'inputmode': 'numeric',
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Enter account number',
                    'title': 'Account number must be between 6 and 20 digits.'
                }
            ),
            'routing_number': forms.TextInput(
                attrs={
                    'pattern': '^\d{9}$',
                    'maxlength': '9', 
                    'minlength': '9',
                    'inputmode': 'numeric',
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Enter routing number',
                     'title': 'Routing number must be exactly 9 digits.'
                }
            ),
            'validity': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Enter validity',
                    'title': 'Please enter the validity of the account',
                }
            ),
        }

    def clean_account_number(self):
        account_number = self.cleaned_data['account_number']
        # Add your validation logic for the account number field here
        # For example, you can check for the required format or length
        if len(account_number) < 10:
            raise forms.ValidationError("Account number must be at least 10 characters long.")
        return account_number

    def clean_routing_number(self):
        routing_number = self.cleaned_data['routing_number']
        # Add your validation logic for the routing number field here
        # For example, you can check for the required format or length
        if len(routing_number) < 9:
            raise forms.ValidationError("Routing number must be at least 9 characters long.")
        return routing_number

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_type', 'name_on_card', 'card_number', 'expiration_date', 'cvv']
        widgets = {
            'card_type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'name_on_card': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'pattern': '[0-9]{16}', 'inputmode': 'numeric','maxlength': '16'}),
            'expiration_date': forms.TextInput(attrs={'class': 'form-control form-control-sm','pattern': r'(0[1-9]|1[0-2])\/\d{2}',  'placeholder': 'MM/YY'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'pattern': '[0-9]{3}', 'inputmode': 'numeric','maxlength': '3'}),
        }
        help_texts = {
            'name_on_card': 'Please enter the same name as it appears on your card',
            'card_number': 'Please enter a valid card number (without spaces or dashes).',
            'expiration_date': 'Please enter date in MM/YY format as it appears on your card',
            'cvv': 'Please enter the 3-digit CVV number at the back of your card.',
        }

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if not expiration_date or len(expiration_date) != 5:
            raise forms.ValidationError('Please enter a valid expiration date in MM/YY format.')
        return expiration_date
    
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not card_number or not card_number.isdigit():
            raise ValidationError('Please enter a valid card number (without spaces or dashes).')
        return card_number
    
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if cvv is None:
            raise ValidationError('Please enter the 3-digit CVV number at the back of your card.')
        cvv_str = str(cvv)
        if not cvv_str.isdigit() or len(cvv_str) != 3:
            raise ValidationError('Please enter a valid 3-digit CVV number.')
        return cvv

class EWalletForm(forms.ModelForm):
    class Meta:
        model = EWallet
        fields = ['e_wallet_name', 'account_email']
        
        widgets = {
            'e_wallet_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'account_email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'}),
        }

        help_texts = {
            'account_email': 'Please enter a valid email address.',
        }
        
class CheckByEmailForm(forms.ModelForm):
    class Meta:
        model = CheckByEmail
        fields = ['poBox', 'use_basicInfo_address']
        
        widgets = {
            'poBox': forms.TextInput(attrs={'class': 'form-control form-control-sm ', 'pattern': r'^[0-9a-zA-Z\s\-,.]*$'}),
            'use_basicInfo_address': forms.CheckboxInput(attrs={'class': 'form-check-input '}),
        }

        help_texts = {
            'poBox': 'Please enter a valid PO Box address.',
        }
        
        
class RidePreferenceForm(forms.ModelForm):
    class Meta:
        model = RidePreference
        fields = ['ride_preference']

        widgets = {
            'ride_preference': forms.RadioSelect(attrs={'class': 'form-check-input'}), 
        }
        help_texts = {
            'ride_preference': 'Please select your ride preference.',
        }
        
class TaxDocumentSettingForm(forms.ModelForm):
    class Meta:
        model = TaxDocumentSetting
        fields = ['taxUserType', 'formType', 'uploadedDocuments']
        widgets = {
            'taxUserType': forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'taxUserTypeSelect'}),
            'formType': forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'formTypeSelect'}),
            'uploadedDocuments': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        
        

