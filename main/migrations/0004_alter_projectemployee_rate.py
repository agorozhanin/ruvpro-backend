# Generated by Django 4.0.4 on 2022-07-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_alter_project_work_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectemployee',
            name='rate',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Ставка рабочего'),
        ),
    ]
