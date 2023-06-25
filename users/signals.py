from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import Profile

@receiver(post_save, sender=get_user_model())
def update_user_type(sender, instance, created, **kwargs):
    if created:
        
        user_type = instance.user_type
       # print(user_type)
        
        if user_type == 'employee':
            employee_group, _ = Group.objects.get_or_create(name='employee')
            employee_group.user_set.add(instance)
            
        elif user_type == 'employer':
            employer_group, _ = Group.objects.get_or_create(name='employer')
            employer_group.user_set.add(instance)

        instance.save()
 
@receiver(post_save, sender=get_user_model())
def update_profile_account_created(sender, instance, created, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.account_created = True
        profile.save()