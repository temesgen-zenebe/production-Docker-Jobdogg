# Generated by Django 4.2 on 2023-06-26 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0036_alter_skillsettestresult_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='OnProgressSkillTest_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='Skipped_completed',
            field=models.BooleanField(default=False),
        ),
    ]
