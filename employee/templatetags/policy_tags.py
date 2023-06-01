from django import template
from employee.models import UserAcceptedPolicies

register = template.Library()

@register.filter
def check_accepted_policy(user_accepted_policies, policy):
    try:
        user_accepted_policy = user_accepted_policies.get(policies=policy)
        return user_accepted_policy.accepted
    except UserAcceptedPolicies.DoesNotExist:
        return False
    
