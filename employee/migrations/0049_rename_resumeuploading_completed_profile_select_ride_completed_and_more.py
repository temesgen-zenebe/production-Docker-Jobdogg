# Generated by Django 4.2 on 2023-07-23 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0048_background_check_expiration_states_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='ResumeUploading_completed',
            new_name='Select_Ride_completed',
        ),
        migrations.AddField(
            model_name='profile',
            name='Treat_Box_completed',
            field=models.BooleanField(default=False),
        ),
    ]
