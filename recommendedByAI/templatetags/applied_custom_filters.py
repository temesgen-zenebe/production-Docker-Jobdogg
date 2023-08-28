from django import template
from recommendedByAI.models import AppliedJobHistory

register = template.Library()

@register.filter
def has_applied(job, user):
    return AppliedJobHistory.objects.filter(job=job, user=user, status='applied').exists()