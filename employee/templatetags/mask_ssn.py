from django.template import Library
register = Library()

@register.filter
def mask_ssn(value):
    if value:
        masked_value = '#' * 5 + value[5:]  # Replace the first five digits with "#" signs
        return masked_value[:3] + '-' + masked_value[3:5] + '-' + value[-4:]
    return ''
