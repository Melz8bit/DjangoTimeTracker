# Generated by Django 3.2.7 on 2021-09-21 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0006_remove_timesheet_total_hours_worked'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='total_hours_worked',
            field=models.IntegerField(default=0),
        ),
    ]