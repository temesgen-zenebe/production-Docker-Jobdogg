from django import forms
from employee.models import Category, Position


class JobFilterForm(forms.Form):
    industry = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Any Industry")
    job_title = forms.ModelChoiceField(queryset=Position.objects.all(), empty_label="Any Job Title")
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=2, required=False)
    min_experience = forms.IntegerField(min_value=0, required=False)
    # Add more fields for other criteria