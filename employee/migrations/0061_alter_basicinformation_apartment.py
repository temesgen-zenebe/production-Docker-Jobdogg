# Generated by Django 4.2 on 2023-09-07 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0060_alter_language_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinformation',
            name='apartment',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
