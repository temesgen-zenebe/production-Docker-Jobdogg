from django import forms
from .models import JobRequisition
from employee.models import Category, Position, Skill  # Make sure to import these models
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
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm','rows': 3}),
            'representative_full_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'Department': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'website': forms.URLInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'fax': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'google_map_link': forms.URLInput(attrs={'class': 'form-control form-control-sm'}),
        }
        help_texts = {
             'opening_hours':'eg. Weekend Hours (Mon-Fri 9:00 AM - 5:00 PM) & Weekday Hours (Sat-Sun 3:00 AM - 2:00 PM).'
        }
   

class JobRequisitionForm(forms.ModelForm):
    industry = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-control form-control-sm my-2', 'id': 'id_industry' })
    )
    job_title = forms.ModelChoiceField(
        queryset=Position.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select form-control form-control-sm my-2', 'id': 'id_job_title'})
    )
    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select form-control form-control-sm my-2', 'id': 'id_required_skills'}),
        help_text="Select multiple options by holding down the Ctrl key (or Command key on Mac)."
    )
    
   
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if 'industry' in self.data:
            try:
                industry_id = int(self.data.get('industry'))
                self.fields['job_title'].queryset = Position.objects.filter(category_id=industry_id)
            except (ValueError, TypeError):
                pass

        if 'job_title' in self.data:
            try:
                job_title_ids = map(int, self.data.getlist('job_title'))
                self.fields['required_skills'].queryset = Skill.objects.filter(position__in=job_title_ids)
                
            except (ValueError, TypeError):
                pass
        
    class Meta:
        model = JobRequisition
        fields = (
            'custom_job_title','custom_required_skills',
            'department','min_experience', 'min_degree_requirements', 
            'job_type', 'salary_type','min_salary_amount', 'max_salary_amount', 
            'work_arrangement_preference','relocatable', 'city', 'state', 'zip_code', 
            'address1', 'certifications_required','star_rating', 'contact_person', 
            'contact_email','from_date','to_date','start_time', 'end_time','job_description',
           'preference_action',
        )
        labels = {
            'custom_required_skills': 'Additional Required Skills',
            'relocatable': 'Are you willing to relocate?',
            'min_experience': 'Minimum Experience',
            'preference_action': 'Preference Action',
            'custom_job_title': 'Custom Job Title',
            'department': 'Department',
            'min_experience': 'Minimum Experience',
            'min_degree_requirements': 'Minimum Degree Requirements',
            'job_type': 'Job Type',
            'salary_type': 'Salary Type',
            'min_salary_amount': 'Minimum Salary Amount',
            'max_salary_amount': 'Maximum Salary Amount',
            'work_arrangement_preference': 'Work Arrangement Preference',
            'relocatable': 'Relocatable',
            'city': 'City',
            'state': 'State',
            'zip_code': 'ZIP Code',
            'address1': 'Address Line 1',
            'certifications_required': 'Required Certifications',
            'star_rating': 'Star Rating',
            'contact_person': 'Contact Person',
            'contact_email': 'Contact Email',
            'from_date': 'Start Date',
            'to_date': 'End Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
            'job_description': 'Job Description',
            'preference_action': 'Preference Action',
            # Add labels for other fields here
        }

        widgets = {
            'custom_job_title': forms.TextInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'department': forms.TextInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'custom_required_skills': forms.Textarea(attrs={'class': 'form-control form-control-sm my-2', 'rows': 2}),
            'job_type': forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),
            'salary_type': forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),
            'min_degree_requirements': forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),
            'min_experience': forms.NumberInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control form-control-sm my-2', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'state': forms.TextInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'address1': forms.TextInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'certifications_required': forms.Textarea(attrs={'class': 'form-control form-control-sm my-2', 'rows': 3}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'from_date': forms.DateInput(attrs={'class': 'form-control form-control-sm my-2', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control form-control-sm my-2', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control form-control-sm my-2', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control form-control-sm my-2', 'type': 'time'}),
            'min_salary_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'max_salary_amount': forms.NumberInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'work_arrangement_preference': forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),
            'relocatable': forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),
            'star_rating': forms.NumberInput(attrs={'class': 'form-control form-control-sm my-2'}),
            'preference_action': forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),

            # Customize other widgets as needed
        }

        help_texts = {
            'custom_job_title':"If the job title you're looking for isn't found in the options, input your own custom job title.",
            'custom_required_skills':"you can add more custom skills ",
            'certifications_required':"If any listed out the required Certification",
        }
   
   
