# Generated by Django 4.0.4 on 2022-07-06 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_project_sum_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectemployee',
            name='rate',
        ),
    ]
