from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import EmployeePreferences, SkillSetTestResult
from employer.models import JobRequisition
from recommendedByAI.models import RecommendedJobs

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
    elif not created and not instance.desired_positions.exists():
        # Create a default SkillSetTestResult object for the first EmployeePreferences object
        try:
            skill_test_result = SkillSetTestResult.objects.get(user=instance.user, position=None)
            skill_test_result.user = instance.user
            skill_test_result.save()
        except SkillSetTestResult.DoesNotExist:
            SkillSetTestResult.objects.create(
                user=instance.user,
                skill_test=last_skill_test_link if last_skill_test_link else ''
            )



"""@receiver(post_save, sender=EmployeePreferences)
def generate_recommended_jobs(sender, instance, created, **kwargs):
    if created:
        # Get positions and skills from the instance
        positions = instance.get_positions()
        skills = instance.get_skills()

        # Get relevant job requisitions based on positions and skills
        relevant_jobs = JobRequisition.objects.filter(
            job_title__in=positions,
            required_skills__in=skills
        ).distinct()

        # Save the relevant jobs to RecommendedJobs
        for job in relevant_jobs:
            RecommendedJobs.objects.create(
                employee_preferences=instance,
                job_requisition=job
            )"""
