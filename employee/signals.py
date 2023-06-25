from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmployeePreferences, Position, SkillSetTestResult

#@receiver(post_save, sender=EmployeePreferences)
def create_or_update_skill_test_result(sender, instance, created, **kwargs):
    if created:
        # Fetch the desired user and desired positions
        user = instance.user
        desired_positions = instance.desired_positions.all()
        for position in desired_positions:
            print(position.position)
            print(position.category)
            print(position.skill_test_link)
       
        # Retrieve the last created position from desired_positions
        last_position = desired_positions.order_by('-created').first()
        print(last_position)
        if last_position:
            # Create a new SkillSetTestResult object
            skill_test_result = SkillSetTestResult.objects.create(
                user=user,
                position=last_position,
                skill_test=last_position.skill_test_link,
            )
       
    else:
        # Update the existing SkillSetTestResult objects
        skill_test_results = SkillSetTestResult.objects.filter(user=instance.user)
        skill_test_results.update(user=instance.user)