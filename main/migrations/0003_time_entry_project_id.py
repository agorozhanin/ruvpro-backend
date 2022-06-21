# Generated by Django 4.0.4 on 2022-06-20 00:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0002_employee_statistics_income_project_average_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='time_entry',
            name='project_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.project',
                                    verbose_name='ID Проекта'),
        ),
    ]