# Generated by Django 4.2 on 2023-07-13 18:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0041_videoresume_rettingcommenting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rettingcommenting',
            name='retting',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='rettingcommenting',
            name='tag',
            field=models.CharField(choices=[('like', 'like'), ('dislike', 'dislike'), ('good', 'good'), ('bast', 'bast'), ('qualified', 'qualified')], max_length=50),
        ),
    ]
