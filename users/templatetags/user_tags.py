from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def is_admin(user):
    employee_group = Group.objects.get(name='admin')
    return employee_group in user.groups.all()

@register.filter
def is_employee(user):
    employee_group = Group.objects.get(name='employee')
    return employee_group in user.groups.all()

@register.filter
def is_employer(user):
    employee_group = Group.objects.get(name='employer')
    return employee_group in user.groups.all()