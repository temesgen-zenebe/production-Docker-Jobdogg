from django import template
from django.template.defaultfilters import phone2numeric

register = template.Library()

@register.filter
def format_phone_number(value):
    # Remove any non-digit characters from the phone number
    phone_number = ''.join(filter(str.isdigit, str(value)))

    # Apply the desired phone number format (e.g., XXX-XXX-XXXX)
    formatted_number = '-'.join([phone_number[:3], phone_number[3:6], phone_number[6:]])

    return formatted_number
