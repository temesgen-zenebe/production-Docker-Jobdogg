from django import forms
from datetime import datetime
from .models import Personal, Language


class PersonalForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['languages'].queryset = Language.objects.all()  # Update the queryset for the 'languages' field
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
            'date_of_birth': forms.DateInput(attrs={'type': 'date','style': 'width: 100%; font-size:13px;'}), 
        }
        
        