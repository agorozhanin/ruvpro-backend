# Generated by Django 4.0.4 on 2022-07-05 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_appuser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectemployee',
            name='assists_work_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Суммарное рабочее время всех подсобных проекта'),
        ),
        migrations.AddField(
            model_name='projectemployee',
            name='interns_work_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Суммарное рабочее время всех интернов проекта'),
        ),
        migrations.AddField(
            model_name='projectemployee',
            name='masters_work_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Суммарное рабочее время всех мастеров проекта'),
        ),
        migrations.AddField(
            model_name='projectemployee',
            name='mentors_work_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Суммарное рабочее время всех менторов проекта'),
        ),
        migrations.AddField(
            model_name='projectemployee',
            name='pupils_work_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Суммарное рабочее время всех учеников проекта'),
        ),
        migrations.AlterField(
            model_name='projectemployee',
            name='work_time',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Суммарное рабочее время'),
        ),
    ]
