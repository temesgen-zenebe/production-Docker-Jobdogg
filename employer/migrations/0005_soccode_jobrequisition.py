# Generated by Django 4.2 on 2023-08-20 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0058_alter_employeepreferences_job_type'),
        ('employer', '0004_employerpoliciesandterms_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soc_code', models.CharField(max_length=200)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soc_code', to='employee.position')),
            ],
        ),
        migrations.CreateModel(
            name='JobRequisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=255)),
                ('required_skills', models.TextField()),
                ('min_experience', models.PositiveIntegerField()),
                ('min_degree_requirements', models.CharField(max_length=100)),
                ('job_type', models.CharField(choices=[('Temp', 'Temporary'), ('Temp-Perm', 'Temporary to Permanent'), ('Perm', 'Permanent'), ('full-time', 'Full-time'), ('part-time', 'Part-time'), ('contract', 'Contract/Freelance'), ('internship', 'Internship'), ('apprenticeship', 'Apprenticeship'), ('remote', 'Remote/Telecommute'), ('shift-based', 'Shift-based'), ('consultant', 'Consultant'), ('other', 'Other')], max_length=20)),
                ('salary_type', models.CharField(choices=[('annual', 'Annual Salary'), ('monthly', 'Monthly Salary'), ('twoWeeks', 'Two Weeks Salary'), ('weekly', 'Weekly Salary'), ('daily', 'Daily Rate'), ('hourly', 'Hourly Wage'), ('commission', 'Commission'), ('bonus', 'Bonus'), ('profit_sharing', 'Profit Sharing'), ('other', 'Other')], max_length=20)),
                ('min_salary_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_salary_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('work_arrangement_preference', models.CharField(choices=[('REMOTE', 'Remote'), ('ON_SITE', 'On-site'), ('HYBRID', 'Hybrid')], default='REMOTE', max_length=10)),
                ('relocatable', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=10)),
                ('address1', models.CharField(max_length=255)),
                ('certifications_required', models.TextField(blank=True)),
                ('star_rating', models.PositiveIntegerField()),
                ('contact_person', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('job_description', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industry', to='employee.category')),
                ('job_title', models.ManyToManyField(to='employee.position')),
                ('skills', models.ManyToManyField(to='employee.skill')),
                ('soc_code', models.ManyToManyField(to='employer.soccode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
