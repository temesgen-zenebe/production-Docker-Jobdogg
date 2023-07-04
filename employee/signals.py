from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import EmployeePreferences, SkillSetTestResult

@receiver(post_save, sender=EmployeePreferences)
def create_or_update_skill_test_results(sender, instance, created, **kwargs):
    if created or instance.desired_positions.exists():
        desired_positions = instance.desired_positions.all()
        last_skill_test_link = desired_positions.order_by('-created').values_list('skill_test_link', flat=True).first()

        for position in desired_positions:
            try:
                skill_test_result = SkillSetTestResult.objects.get(user=instance.user, position=position)
                skill_test_result.skill_test = last_skill_test_link if last_skill_test_link else ''
                skill_test_result.save()
            except SkillSetTestResult.DoesNotExist:
                SkillSetTestResult.objects.create(
                    user=instance.user,
                    position=position,
                    skill_test=last_skill_test_link if last_skill_test_link else ''
                )
