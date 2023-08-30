# Generated by Django 4.2 on 2023-08-27 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employer', '0017_alter_jobrequisition_soc_code_alter_soccode_position'),
        ('employee', '0058_alter_employeepreferences_job_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('employee_preferences', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employeepreferences')),
                ('job_requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employer.jobrequisition')),
            ],
        ),
    ]