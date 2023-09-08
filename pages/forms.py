from django import forms
from django.core.validators import RegexValidator
from .models import Subscriber

class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-sm',
            'id': 'emailAddressBelow',
            'placeholder': 'Email Address',
            'data-sb-validations': 'required'
        }),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                message='Enter a valid email address.',
                code='invalid_email'
            )
        ]
    )

    class Meta:
        model = Subscriber
        fields = ['email']
