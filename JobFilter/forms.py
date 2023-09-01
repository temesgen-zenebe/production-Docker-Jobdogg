from django import forms
from employee.models import Category, Position
from common.utils.chooseConstant import (
    ACTION_TYPES, DEGREE_TYPE_CHOICES, 
    JOB_TYPES, RELOCATION, SALARY_TYPES, 
    WORK_ARRANGEMENT_CHOICES,SORT_CHOICES,
)

class JobFilterForm(forms.Form):
    industry = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Industry'
    )
    job_title = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label='Job Title'
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        label='City'
    )
    state = forms.CharField(
        max_length=2,
        required=False,
        label='State'
    )
    min_experience = forms.IntegerField(
        required=False,
        label='Minimum Experience'
    )
    
    # Use forms.ChoiceField with choices for Select fields
    job_type = forms.ChoiceField(
        choices=JOB_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),
        label='Job Type'
    )
   
    work_arrangement_preference = forms.ChoiceField(
        choices=WORK_ARRANGEMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm my-2'}),
        label='Work Arrangement Preference'
    )
    
    search = forms.CharField(
        max_length=255,
        required=False,
        label='Search'
    )
    
    sorting = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        label='Sort',
    )
