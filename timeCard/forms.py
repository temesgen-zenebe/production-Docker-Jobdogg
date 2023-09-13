from django import forms
from .models import TimeAssigned, DateAssigned, TimeCard

class TimeAssignedForm(forms.ModelForm):
    class Meta:
        model = TimeAssigned
        fields = ['title','start_time', 'end_time', 'lunch_time', 'over_start_time', 'over_end_time', 'total_over_time', 'double_over_time', 'total_hours']
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 100%; font-size: 13px;'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 100%; font-size: 13px;'}),
            'lunch_time': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 100%; font-size: 13px;'}),
            'over_start_time': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 100%; font-size: 13px;'}),
            'over_end_time': forms.TimeInput(attrs={'type': 'time', 'style': 'width: 100%; font-size: 13px;'}),
            'total_over_time': forms.NumberInput(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'double_over_time': forms.NumberInput(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'total_hours': forms.NumberInput(attrs={'style': 'width: 100%; font-size: 13px;'}),
        }

class DateAssignedForm(forms.ModelForm):
    class Meta:
        model = DateAssigned
        fields = ['date_assign', 'time_assign']
        widgets = {
            'date_assign': forms.Select(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'time_assign': forms.Select(attrs={'style': 'width: 100%; font-size: 13px;'}),
        }

class TimeCardForm(forms.ModelForm):
    class Meta:
        model = TimeCard
        fields = ['employee', 'date_assigned','job_type', 'location_URL', 'special_task']
        widgets = {
            'employer': forms.Select(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'employee': forms.TextInput(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'date_assigned': forms.Select(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'location_URL': forms.URLInput(attrs={'style': 'width: 100%; font-size: 13px;'}),
            'special_task': forms.Textarea(attrs={'style': 'width: 100%; font-size: 13px;'}),
        }
