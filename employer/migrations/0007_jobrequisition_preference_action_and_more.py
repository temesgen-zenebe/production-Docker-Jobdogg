# Generated by Django 4.2 on 2023-08-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0006_jobrequisition_custom_job_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequisition',
            name='preference_action',
            field=models.CharField(choices=[('SAVE', 'Save'), ('ALERT', 'Alert'), ('POST', 'Post'), ('ALL', 'All')], default='ALL', max_length=20),
        ),
        migrations.AlterField(
            model_name='jobrequisition',
            name='min_degree_requirements',
            field=models.CharField(choices=[('associate', 'Associate Degree'), ('bachelor', "Bachelor's Degree"), ('master', "Master's Degree"), ('doctorate', 'Doctorate Degree'), ('diploma', 'Diploma'), ('certificate', 'Certificate'), ('other', 'Other')], max_length=100),
        ),
    ]