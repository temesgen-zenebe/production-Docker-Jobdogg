# Generated by Django 4.2 on 2023-06-24 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0035_rename_state_skillsettestresult_states'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillsettestresult',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.position'),
        ),
    ]