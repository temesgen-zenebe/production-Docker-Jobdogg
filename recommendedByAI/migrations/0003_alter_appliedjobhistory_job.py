# Generated by Django 4.2 on 2023-08-29 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendedByAI', '0002_appliedjobhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedjobhistory',
            name='job',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
